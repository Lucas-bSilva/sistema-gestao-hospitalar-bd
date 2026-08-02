from __future__ import annotations

import os
import json
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any

from sqlalchemy import inspect, text

from hospital_yuska.banco import sessao_transacional
from hospital_yuska.consultas.avancadas import (
    listar_preceptores_de_pacientes_flamenguistas,
    obter_atendimento_eager,
    obter_atendimento_lazy,
    percentual_alto_risco_por_residente,
    ultimo_atendimento_de_cada_paciente,
)
from hospital_yuska.repositorios.operacoes_etapa1 import (
    atualizar_paciente,
    calcular_media_duracao_por_residente,
    inserir_atendimento,
    listar_atendimentos_paciente,
    listar_procedimentos_atendimento,
    pacientes_sem_procedimento_alto_risco,
    preceptores_com_mais_de_cinco_supervisoes,
    quantidade_plantoes_por_unidade,
    ranking_residentes,
    remover_procedimento_nao_faturado,
)


Registro = dict[str, Any]


def _converter_linhas(linhas: Any) -> list[Registro]:
    return [
        dict(linha._mapping)
        for linha in linhas
    ]


def _limites_mes_atual() -> tuple[date, date]:
    inicio = date.today().replace(day=1)

    if inicio.month == 12:
        fim = date(inicio.year + 1, 1, 1)
    else:
        fim = date(
            inicio.year,
            inicio.month + 1,
            1,
        )

    return inicio, fim


def verificar_objetos_banco() -> list[Registro]:
    objetos = {
        "Tabela de internações":
            "public.internacao",
        "Tabela de auditoria":
            "public.auditoria_atendimento",
        "View de pacientes internados":
            "public.vw_pacientes_internados",
        "View de supervisão":
            "public.vw_residentes_sem_supervisor",
        "View de estatísticas":
            "public.vw_estatisticas_atendimentos_mensal",
    }

    registros: list[Registro] = []

    with sessao_transacional() as sessao:
        for descricao, objeto in objetos.items():
            encontrado = sessao.scalar(
                text(
                    "SELECT to_regclass(:objeto)"
                ),
                {"objeto": objeto},
            )

            registros.append(
                {
                    "categoria": "Objeto do banco",
                    "nome": descricao,
                    "status": (
                        "Disponível"
                        if encontrado is not None
                        else "Ausente"
                    ),
                }
            )

        rotinas = sessao.execute(
            text(
                """
                SELECT routine_name
                FROM information_schema.routines
                WHERE routine_schema = 'public'
                  AND routine_name IN (
                      'sp_registrar_atendimento_completo',
                      'sp_calcular_tempo_medio_espera',
                      'sp_reajustar_escala'
                  )
                ORDER BY routine_name
                """
            )
        ).scalars().all()

        for rotina in (
            "sp_registrar_atendimento_completo",
            "sp_calcular_tempo_medio_espera",
            "sp_reajustar_escala",
        ):
            registros.append(
                {
                    "categoria": "Stored procedure",
                    "nome": rotina,
                    "status": (
                        "Disponível"
                        if rotina in rotinas
                        else "Ausente"
                    ),
                }
            )

        triggers = sessao.execute(
            text(
                """
                SELECT trigger_name
                FROM information_schema.triggers
                WHERE trigger_schema = 'public'
                ORDER BY trigger_name
                """
            )
        ).scalars().all()

        for trigger in (
            "trg_check_sobreposicao_escala",
            "trg_audita_atendimento",
            "trg_atualiza_media_procedimentos",
        ):
            registros.append(
                {
                    "categoria": "Trigger",
                    "nome": trigger,
                    "status": (
                        "Disponível"
                        if trigger in triggers
                        else "Ausente"
                    ),
                }
            )

    return registros


def inserir_atendimento_orm(
    *,
    data_hora: datetime,
    duracao_minutos: int,
    id_paciente: int,
    id_residente: int,
    id_preceptor: int,
    id_unidade: int,
) -> list[Registro]:
    with sessao_transacional() as sessao:
        atendimento = inserir_atendimento(
            sessao,
            data_hora=data_hora,
            duracao_minutos=duracao_minutos,
            id_paciente=id_paciente,
            id_residente=id_residente,
            id_preceptor=id_preceptor,
            id_unidade=id_unidade,
        )

        return [
            {
                "id_atendimento":
                    atendimento.id_atendimento,
                "data_hora":
                    atendimento.data_hora,
                "duracao_minutos":
                    atendimento.duracao_minutos,
                "id_paciente":
                    atendimento.id_paciente,
                "id_residente":
                    atendimento.id_residente,
                "id_preceptor":
                    atendimento.id_preceptor,
                "id_unidade":
                    atendimento.id_unidade,
                "resultado":
                    "Atendimento inserido",
            }
        ]


def listar_atendimentos_orm(
    id_paciente: int,
) -> list[Registro]:
    with sessao_transacional() as sessao:
        atendimentos = listar_atendimentos_paciente(
            sessao,
            id_paciente,
        )

        return [
            {
                "id_atendimento":
                    atendimento.id_atendimento,
                "data_hora":
                    atendimento.data_hora,
                "duracao_minutos":
                    atendimento.duracao_minutos,
                "paciente":
                    atendimento.paciente.pessoa.nome,
                "residente":
                    atendimento
                    .residente
                    .profissional
                    .pessoa
                    .nome,
                "preceptor":
                    atendimento
                    .preceptor
                    .profissional
                    .pessoa
                    .nome,
                "unidade":
                    atendimento.unidade.nome,
            }
            for atendimento in atendimentos
        ]


def listar_procedimentos_orm(
    id_atendimento: int,
) -> list[Registro]:
    with sessao_transacional() as sessao:
        realizados = listar_procedimentos_atendimento(
            sessao,
            id_atendimento,
        )

        return [
            {
                "id_atendimento":
                    realizado.id_atendimento,
                "id_procedimento":
                    realizado.id_procedimento,
                "procedimento":
                    realizado.procedimento.nome,
                "quantidade":
                    realizado.quantidade,
                "tempo_real_minutos":
                    realizado.tempo_real_minutos,
                "faturado":
                    realizado.faturado,
                "observacao":
                    realizado.observacao,
            }
            for realizado in realizados
        ]


def atualizar_paciente_orm(
    *,
    id_paciente: int,
    endereco: str | None,
    num_convenio: str | None,
) -> list[Registro]:
    with sessao_transacional() as sessao:
        paciente = atualizar_paciente(
            sessao,
            id_paciente,
            endereco=endereco,
            num_convenio=num_convenio,
        )

        return [
            {
                "id_paciente":
                    paciente.id_pessoa,
                "endereco":
                    paciente.endereco,
                "num_convenio":
                    paciente.num_convenio,
                "resultado":
                    "Paciente atualizado",
            }
        ]


def remover_procedimento_orm(
    *,
    id_atendimento: int,
    id_procedimento: int,
) -> list[Registro]:
    with sessao_transacional() as sessao:
        removido = remover_procedimento_nao_faturado(
            sessao,
            id_atendimento,
            id_procedimento,
        )

        return [
            {
                "id_atendimento":
                    id_atendimento,
                "id_procedimento":
                    id_procedimento,
                "resultado": (
                    "Procedimento removido"
                    if removido
                    else "Procedimento não encontrado"
                ),
            }
        ]


def obter_media_duracao() -> list[Registro]:
    with sessao_transacional() as sessao:
        return _converter_linhas(
            calcular_media_duracao_por_residente(
                sessao
            )
        )


def obter_ranking_residentes() -> list[Registro]:
    with sessao_transacional() as sessao:
        return _converter_linhas(
            ranking_residentes(sessao)
        )


def obter_preceptores_mais_cinco() -> list[Registro]:
    inicio, fim = _limites_mes_atual()

    with sessao_transacional() as sessao:
        return _converter_linhas(
            preceptores_com_mais_de_cinco_supervisoes(
                sessao,
                datetime.combine(
                    inicio,
                    datetime.min.time(),
                ),
                datetime.combine(
                    fim,
                    datetime.min.time(),
                ),
            )
        )


def obter_plantoes_mes_atual() -> list[Registro]:
    inicio, fim = _limites_mes_atual()

    with sessao_transacional() as sessao:
        return _converter_linhas(
            quantidade_plantoes_por_unidade(
                sessao,
                inicio,
                fim,
            )
        )


def obter_pacientes_sem_alto_risco() -> list[Registro]:
    with sessao_transacional() as sessao:
        return _converter_linhas(
            pacientes_sem_procedimento_alto_risco(
                sessao
            )
        )


def obter_preceptores_flamenguistas() -> list[Registro]:
    with sessao_transacional() as sessao:
        return _converter_linhas(
            listar_preceptores_de_pacientes_flamenguistas(
                sessao
            )
        )


def obter_ultimos_atendimentos() -> list[Registro]:
    with sessao_transacional() as sessao:
        atendimentos = (
            ultimo_atendimento_de_cada_paciente(
                sessao
            )
        )

        registros: list[Registro] = []

        for atendimento in atendimentos:
            procedimentos = ", ".join(
                realizado.procedimento.nome
                for realizado
                in atendimento.procedimentos_realizados
            )

            registros.append(
                {
                    "paciente":
                        atendimento.paciente.pessoa.nome,
                    "data_hora":
                        atendimento.data_hora,
                    "residente":
                        atendimento
                        .residente
                        .profissional
                        .pessoa
                        .nome,
                    "preceptor":
                        atendimento
                        .preceptor
                        .profissional
                        .pessoa
                        .nome,
                    "procedimentos":
                        procedimentos or "Nenhum",
                }
            )

        return registros


def obter_percentual_alto_risco() -> list[Registro]:
    with sessao_transacional() as sessao:
        return _converter_linhas(
            percentual_alto_risco_por_residente(
                sessao
            )
        )


def demonstrar_lazy_eager(
    id_atendimento: int,
) -> list[Registro]:
    registros: list[Registro] = []

    with sessao_transacional() as sessao:
        atendimento = obter_atendimento_lazy(
            sessao,
            id_atendimento,
        )

        if atendimento is None:
            raise ValueError(
                "Atendimento não encontrado."
            )

        antes = (
            "procedimentos_realizados"
            in inspect(atendimento).unloaded
        )

        quantidade = len(
            atendimento.procedimentos_realizados
        )

        depois = (
            "procedimentos_realizados"
            in inspect(atendimento).unloaded
        )

        registros.append(
            {
                "estrategia": "Lazy loading",
                "nao_carregado_antes": antes,
                "quantidade": quantidade,
                "nao_carregado_depois": depois,
            }
        )

    with sessao_transacional() as sessao:
        atendimento = obter_atendimento_eager(
            sessao,
            id_atendimento,
        )

        if atendimento is None:
            raise ValueError(
                "Atendimento não encontrado."
            )

        carregado = (
            "procedimentos_realizados"
            not in inspect(atendimento).unloaded
        )

        registros.append(
            {
                "estrategia": "Eager loading",
                "nao_carregado_antes": False,
                "quantidade": len(
                    atendimento.procedimentos_realizados
                ),
                "nao_carregado_depois":
                    not carregado,
            }
        )

    return registros


def consultar_view(
    nome_view: str,
) -> list[Registro]:
    permitidas = {
        "vw_pacientes_internados",
        "vw_residentes_sem_supervisor",
        "vw_estatisticas_atendimentos_mensal",
    }

    if nome_view not in permitidas:
        raise ValueError(
            "View não autorizada."
        )

    with sessao_transacional() as sessao:
        resultado = sessao.execute(
            text(
                f"SELECT * FROM {nome_view}"
            )
        )

        return [
            dict(registro)
            for registro in resultado.mappings()
        ]


def registrar_atendimento_completo(
    *,
    data_hora: datetime,
    duracao_minutos: int,
    id_paciente: int,
    id_residente: int,
    id_preceptor: int,
    id_unidade: int,
    procedimentos_json: str,
) -> list[Registro]:
    procedimentos = json.loads(
        procedimentos_json
    )

    if not isinstance(procedimentos, list):
        raise ValueError(
            "Os procedimentos devem ser um array JSON."
        )

    with sessao_transacional() as sessao:
        sessao.execute(
            text(
                """
                CALL sp_registrar_atendimento_completo(
                    :data_hora,
                    :duracao_minutos,
                    :id_paciente,
                    :id_residente,
                    :id_preceptor,
                    :id_unidade,
                    CAST(:procedimentos AS JSONB)
                )
                """
            ),
            {
                "data_hora": data_hora,
                "duracao_minutos":
                    duracao_minutos,
                "id_paciente": id_paciente,
                "id_residente": id_residente,
                "id_preceptor": id_preceptor,
                "id_unidade": id_unidade,
                "procedimentos":
                    json.dumps(procedimentos),
            },
        )

    return [
        {
            "resultado":
                "Atendimento completo registrado",
            "procedimentos":
                len(procedimentos),
        }
    ]


def calcular_tempo_medio_espera() -> list[Registro]:
    nome_cursor = (
        "resultado_tempo_espera_desktop"
    )

    with sessao_transacional() as sessao:
        sessao.execute(
            text(
                """
                CALL sp_calcular_tempo_medio_espera(
                    :nome_cursor
                )
                """
            ),
            {"nome_cursor": nome_cursor},
        )

        resultado = sessao.execute(
            text(
                'FETCH ALL FROM '
                '"resultado_tempo_espera_desktop"'
            )
        )

        return [
            dict(registro)
            for registro in resultado.mappings()
        ]


def reajustar_escala(
    *,
    id_residente: int,
    dia_origem: str,
    turno_origem: str,
    dia_destino: str,
    turno_destino: str,
) -> list[Registro]:
    with sessao_transacional() as sessao:
        sessao.execute(
            text(
                """
                CALL sp_reajustar_escala(
                    :id_residente,
                    :dia_origem,
                    :turno_origem,
                    :dia_destino,
                    :turno_destino
                )
                """
            ),
            {
                "id_residente": id_residente,
                "dia_origem": dia_origem,
                "turno_origem": turno_origem,
                "dia_destino": dia_destino,
                "turno_destino": turno_destino,
            },
        )

    return [
        {
            "id_residente": id_residente,
            "origem":
                f"{dia_origem}/{turno_origem}",
            "destino":
                f"{dia_destino}/{turno_destino}",
            "resultado":
                "Escala reajustada",
        }
    ]


def listar_auditoria() -> list[Registro]:
    with sessao_transacional() as sessao:
        resultado = sessao.execute(
            text(
                """
                SELECT
                    id_auditoria,
                    id_atendimento,
                    operacao,
                    usuario,
                    data_hora
                FROM auditoria_atendimento
                ORDER BY id_auditoria DESC
                LIMIT 100
                """
            )
        )

        return [
            dict(registro)
            for registro in resultado.mappings()
        ]


def listar_medias_procedimentos() -> list[Registro]:
    with sessao_transacional() as sessao:
        resultado = sessao.execute(
            text(
                """
                SELECT
                    id_procedimento,
                    codigo,
                    nome,
                    media_tempo_procedimento
                FROM procedimento
                ORDER BY nome
                """
            )
        )

        return [
            dict(registro)
            for registro in resultado.mappings()
        ]


def simular_concorrencia() -> list[Registro]:
    """Executa a simulação de concorrência e retorna sua saída em UTF-8."""

    raiz = Path(__file__).resolve().parents[3]
    arquivo_simulacao = raiz / "scripts" / "simular_concorrencia.py"

    ambiente = os.environ.copy()

    # Padroniza a codificação do processo filho no Windows.
    ambiente["PYTHONUTF8"] = "1"
    ambiente["PYTHONIOENCODING"] = "utf-8"

    processo = subprocess.run(
        [
            sys.executable,
            str(arquivo_simulacao),
        ],
        cwd=raiz,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="strict",
        env=ambiente,
        check=False,
    )

    saida = "\n".join(
        parte
        for parte in (
            processo.stdout.strip(),
            processo.stderr.strip(),
        )
        if parte
    )

    if processo.returncode != 0:
        raise RuntimeError(
            saida
            or "A simulação de concorrência terminou com erro."
        )

    return [
        {"linha": linha}
        for linha in saida.splitlines()
        if linha.strip()
    ]