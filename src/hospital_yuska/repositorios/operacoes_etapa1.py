from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Numeric, cast, exists, func, select
from sqlalchemy.orm import Session, joinedload, selectinload

from hospital_yuska.modelos import (
    Atendimento,
    Escala,
    Paciente,
    Pessoa,
    Preceptor,
    Procedimento,
    ProcedimentoRealizado,
    Profissional,
    Residente,
    Unidade,
)


def inserir_atendimento(
    sessao: Session,
    *,
    data_hora: datetime,
    duracao_minutos: int,
    id_paciente: int,
    id_residente: int,
    id_preceptor: int,
    id_unidade: int,
) -> Atendimento:
    """Insere um atendimento depois de validar as referências."""

    if duracao_minutos <= 0:
        raise ValueError(
            "A duração deve ser positiva."
        )

    if id_residente == id_preceptor:
        raise ValueError(
            "Residente e preceptor devem ser profissionais distintos."
        )

    referencias = (
        (Paciente, id_paciente, "Paciente"),
        (Residente, id_residente, "Residente"),
        (Preceptor, id_preceptor, "Preceptor"),
        (Unidade, id_unidade, "Unidade"),
    )

    for entidade, identificador, nome in referencias:
        if sessao.get(entidade, identificador) is None:
            raise ValueError(
                f"{nome} {identificador} não encontrado."
            )

    atendimento = Atendimento(
        data_hora=data_hora,
        duracao_minutos=duracao_minutos,
        id_paciente=id_paciente,
        id_residente=id_residente,
        id_preceptor=id_preceptor,
        id_unidade=id_unidade,
    )

    sessao.add(atendimento)
    sessao.flush()

    return atendimento


def listar_atendimentos_paciente(
    sessao: Session,
    id_paciente: int,
) -> list[Atendimento]:
    """Lista os atendimentos de um paciente em ordem cronológica."""

    comando = (
        select(Atendimento)

        .where(
            Atendimento.id_paciente == id_paciente
        )

        .options(
            joinedload(
                Atendimento.paciente
            ).joinedload(
                Paciente.pessoa
            ),

            joinedload(
                Atendimento.residente
            ).joinedload(
                Residente.profissional
            ).joinedload(
                Profissional.pessoa
            ),

            joinedload(
                Atendimento.preceptor
            ).joinedload(
                Preceptor.profissional
            ).joinedload(
                Profissional.pessoa
            ),

            joinedload(
                Atendimento.unidade
            ),

            selectinload(
                Atendimento.procedimentos_realizados
            ).joinedload(
                ProcedimentoRealizado.procedimento
            ),
        )

        .order_by(
            Atendimento.data_hora
        )
    )

    return list(
        sessao.scalars(comando).unique()
    )


def listar_procedimentos_atendimento(
    sessao: Session,
    id_atendimento: int,
) -> list[ProcedimentoRealizado]:
    """Lista os procedimentos realizados em um atendimento."""

    comando = (
        select(ProcedimentoRealizado)

        .where(
            ProcedimentoRealizado.id_atendimento ==
            id_atendimento
        )

        .options(
            joinedload(
                ProcedimentoRealizado.procedimento
            )
        )

        .order_by(
            ProcedimentoRealizado.id_procedimento
        )
    )

    return list(
        sessao.scalars(comando)
    )


def atualizar_paciente(
    sessao: Session,
    id_paciente: int,
    *,
    endereco: str | None = None,
    num_convenio: str | None = None,
) -> Paciente:
    """Atualiza endereço e convênio do paciente."""

    paciente = sessao.get(
        Paciente,
        id_paciente,
    )

    if paciente is None:
        raise ValueError(
            f"Paciente {id_paciente} não encontrado."
        )

    if endereco is not None:
        paciente.endereco = endereco

    if num_convenio is not None:
        paciente.num_convenio = num_convenio

    sessao.flush()

    return paciente


def remover_procedimento_nao_faturado(
    sessao: Session,
    id_atendimento: int,
    id_procedimento: int,
) -> bool:
    """Remove um procedimento somente quando não estiver faturado."""

    realizado = sessao.get(
        ProcedimentoRealizado,
        (
            id_atendimento,
            id_procedimento,
        ),
    )

    if realizado is None:
        return False

    if realizado.faturado:
        raise ValueError(
            "O procedimento está faturado e não pode ser removido."
        )

    sessao.delete(realizado)
    sessao.flush()

    return True


def calcular_media_duracao_por_residente(
    sessao: Session,
):
    """Calcula duração média e quantidade de atendimentos."""

    comando = (
        select(
            Residente.id_profissional.label(
                "id_residente"
            ),

            Pessoa.nome.label(
                "residente"
            ),

            func.round(
                cast(
                    func.avg(
                        Atendimento.duracao_minutos
                    ),
                    Numeric(10, 2),
                ),
                2,
            ).label(
                "media_duracao_minutos"
            ),

            func.count(
                Atendimento.id_atendimento
            ).label(
                "total_atendimentos"
            ),
        )

        .join(
            Pessoa,
            Pessoa.id_pessoa ==
            Residente.id_profissional,
        )

        .join(
            Atendimento,
            Atendimento.id_residente ==
            Residente.id_profissional,
        )

        .group_by(
            Residente.id_profissional,
            Pessoa.nome,
        )

        .order_by(
            func.avg(
                Atendimento.duracao_minutos
            ).desc(),

            Pessoa.nome,
        )
    )

    return sessao.execute(comando).all()


def ranking_residentes(
    sessao: Session,
):
    """Classifica residentes pela quantidade de atendimentos."""

    total = func.count(
        Atendimento.id_atendimento
    ).label(
        "total_atendimentos"
    )

    contagens = (
        select(
            Residente.id_profissional.label(
                "id_residente"
            ),

            Pessoa.nome.label(
                "residente"
            ),

            total,
        )

        .join(
            Pessoa,
            Pessoa.id_pessoa ==
            Residente.id_profissional,
        )

        .outerjoin(
            Atendimento,
            Atendimento.id_residente ==
            Residente.id_profissional,
        )

        .group_by(
            Residente.id_profissional,
            Pessoa.nome,
        )

        .subquery()
    )

    comando = (
        select(
            func.dense_rank()
            .over(
                order_by=
                contagens.c.total_atendimentos.desc()
            )
            .label("posicao"),

            contagens.c.id_residente,
            contagens.c.residente,
            contagens.c.total_atendimentos,
        )

        .order_by(
            contagens.c.total_atendimentos.desc(),
            contagens.c.residente,
        )
    )

    return sessao.execute(comando).all()


def preceptores_com_mais_de_cinco_supervisoes(
    sessao: Session,
    data_inicial: datetime,
    data_final: datetime,
):
    """Lista preceptores com mais de cinco supervisões no período."""

    comando = (
        select(
            Preceptor.id_profissional.label(
                "id_preceptor"
            ),

            Pessoa.nome.label(
                "preceptor"
            ),

            func.count(
                Atendimento.id_atendimento
            ).label(
                "total_supervisoes"
            ),
        )

        .join(
            Pessoa,
            Pessoa.id_pessoa ==
            Preceptor.id_profissional,
        )

        .join(
            Atendimento,
            Atendimento.id_preceptor ==
            Preceptor.id_profissional,
        )

        .where(
            Atendimento.data_hora >= data_inicial,
            Atendimento.data_hora < data_final,
        )

        .group_by(
            Preceptor.id_profissional,
            Pessoa.nome,
        )

        .having(
            func.count(
                Atendimento.id_atendimento
            ) > 5
        )

        .order_by(
            func.count(
                Atendimento.id_atendimento
            ).desc(),

            Pessoa.nome,
        )
    )

    return sessao.execute(comando).all()


def quantidade_plantoes_por_unidade(
    sessao: Session,
    data_inicial: date,
    data_final: date,
):
    """Conta plantões por unidade e residente em um período."""

    comando = (
        select(
            Unidade.nome.label(
                "unidade"
            ),

            Pessoa.nome.label(
                "residente"
            ),

            func.count(
                Escala.id_escala
            ).label(
                "quantidade_plantoes"
            ),
        )

        .join(
            Escala,
            Escala.id_unidade ==
            Unidade.id_unidade,
        )

        .join(
            Residente,
            Residente.id_profissional ==
            Escala.id_residente,
        )

        .join(
            Pessoa,
            Pessoa.id_pessoa ==
            Residente.id_profissional,
        )

        .where(
            Escala.data_plantao >= data_inicial,
            Escala.data_plantao < data_final,
        )

        .group_by(
            Unidade.id_unidade,
            Unidade.nome,
            Pessoa.id_pessoa,
            Pessoa.nome,
        )

        .order_by(
            Unidade.nome,

            func.count(
                Escala.id_escala
            ).desc(),

            Pessoa.nome,
        )
    )

    return sessao.execute(comando).all()


def pacientes_sem_procedimento_alto_risco(
    sessao: Session,
):
    """Lista pacientes sem procedimentos classificados como alto risco."""

    ocorrencia_alto_risco = exists(
        select(1)

        .select_from(
            Atendimento
        )

        .join(
            ProcedimentoRealizado,

            ProcedimentoRealizado.id_atendimento ==
            Atendimento.id_atendimento,
        )

        .join(
            Procedimento,

            Procedimento.id_procedimento ==
            ProcedimentoRealizado.id_procedimento,
        )

        .where(
            Atendimento.id_paciente ==
            Paciente.id_pessoa,

            Procedimento.nivel_risco == "ALTO",
        )
    )

    comando = (
        select(
            Paciente.id_pessoa.label(
                "id_paciente"
            ),

            Pessoa.nome.label(
                "paciente"
            ),

            Paciente.num_convenio,
        )

        .join(
            Pessoa,
            Pessoa.id_pessoa ==
            Paciente.id_pessoa,
        )

        .where(
            ~ocorrencia_alto_risco
        )

        .order_by(
            Pessoa.nome
        )
    )

    return sessao.execute(comando).all()