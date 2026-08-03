from __future__ import annotations

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
    listar_atendimentos_paciente,
    ranking_residentes,
)


def linha() -> None:
    print("-" * 78)


def mostrar_atendimentos() -> None:
    id_paciente = int(
        input("ID do paciente: ")
    )

    with sessao_transacional() as sessao:
        atendimentos = listar_atendimentos_paciente(
            sessao,
            id_paciente,
        )

        if not atendimentos:
            print(
                "Nenhum atendimento encontrado."
            )
            return

        for atendimento in atendimentos:
            print(
                f"ID: {atendimento.id_atendimento} | "
                f"Data: {atendimento.data_hora} | "
                f"Paciente: "
                f"{atendimento.paciente.pessoa.nome} | "
                f"Residente: "
                f"{atendimento.residente.profissional.pessoa.nome} | "
                f"Preceptor: "
                f"{atendimento.preceptor.profissional.pessoa.nome} | "
                f"Unidade: {atendimento.unidade.nome}"
            )


def mostrar_ranking() -> None:
    with sessao_transacional() as sessao:
        for item in ranking_residentes(sessao):
            print(
                f"{item.posicao}º | "
                f"{item.residente} | "
                f"{item.total_atendimentos} atendimento(s)"
            )


def mostrar_preceptores_flamenguistas() -> None:
    with sessao_transacional() as sessao:
        resultados = (
            listar_preceptores_de_pacientes_flamenguistas(
                sessao
            )
        )

        for item in resultados:
            print(
                f"{item.id_preceptor} | "
                f"{item.preceptor}"
            )


def mostrar_ultimos_atendimentos() -> None:
    with sessao_transacional() as sessao:
        resultados = (
            ultimo_atendimento_de_cada_paciente(
                sessao
            )
        )

        for atendimento in resultados:
            procedimentos = ", ".join(
                realizado.procedimento.nome
                for realizado
                in atendimento.procedimentos_realizados
            )

            print(
                f"Paciente: "
                f"{atendimento.paciente.pessoa.nome} | "
                f"Data: {atendimento.data_hora} | "
                f"Residente: "
                f"{atendimento.residente.profissional.pessoa.nome} | "
                f"Preceptor: "
                f"{atendimento.preceptor.profissional.pessoa.nome} | "
                f"Procedimentos: "
                f"{procedimentos or 'nenhum'}"
            )


def mostrar_percentuais() -> None:
    with sessao_transacional() as sessao:
        resultados = (
            percentual_alto_risco_por_residente(
                sessao
            )
        )

        for item in resultados:
            print(
                f"{item.residente}: "
                f"{item.percentual_alto_risco}% | "
                f"alto risco: "
                f"{item.procedimentos_alto_risco} | "
                f"total: {item.total_procedimentos}"
            )


def mostrar_view(
    nome_view: str,
) -> None:
    views_permitidas = {
        "vw_pacientes_internados",
        "vw_residentes_sem_supervisor",
        "vw_estatisticas_atendimentos_mensal",
    }

    if nome_view not in views_permitidas:
        raise ValueError(
            "View não permitida."
        )

    with sessao_transacional() as sessao:
        resultado = sessao.execute(
            text(
                f"SELECT * FROM {nome_view}"
            )
        )

        registros = list(
            resultado.mappings()
        )

        if not registros:
            print(
                "A view não retornou registros."
            )
            return

        for registro in registros:
            print(
                dict(registro)
            )


def demonstrar_lazy_eager() -> None:
    id_atendimento = int(
        input("ID do atendimento: ")
    )

    with sessao_transacional() as sessao:
        atendimento_lazy = obter_atendimento_lazy(
            sessao,
            id_atendimento,
        )

        if atendimento_lazy is None:
            print(
                "Atendimento não encontrado."
            )
            return

        relacao_nao_carregada = (
            "procedimentos_realizados"
            in inspect(atendimento_lazy).unloaded
        )

        print(
            "Lazy loading — relação ainda não carregada:",
            relacao_nao_carregada,
        )

        quantidade = len(
            atendimento_lazy.procedimentos_realizados
        )

        print(
            "Quantidade carregada após o acesso:",
            quantidade,
        )

        print(
            "Relação ainda não carregada depois do acesso:",
            "procedimentos_realizados"
            in inspect(atendimento_lazy).unloaded,
        )

    with sessao_transacional() as sessao:
        atendimento_eager = obter_atendimento_eager(
            sessao,
            id_atendimento,
        )

        if atendimento_eager is None:
            print(
                "Atendimento não encontrado."
            )
            return

        print(
            "Eager loading — relação carregada antecipadamente:",
            "procedimentos_realizados"
            not in inspect(atendimento_eager).unloaded,
        )


def main() -> None:
    opcoes = {
        "1": mostrar_atendimentos,
        "2": mostrar_ranking,
        "3": mostrar_preceptores_flamenguistas,
        "4": mostrar_ultimos_atendimentos,
        "5": mostrar_percentuais,

        "6": lambda: mostrar_view(
            "vw_pacientes_internados"
        ),

        "7": lambda: mostrar_view(
            "vw_residentes_sem_supervisor"
        ),

        "8": lambda: mostrar_view(
            "vw_estatisticas_atendimentos_mensal"
        ),

        "9": demonstrar_lazy_eager,
    }

    while True:
        linha()

        print(
            "Sistema de Gestão Hospitalar "
            "Dra. Yuska — Etapa 2"
        )

        print(
            "1. Atendimentos de um paciente"
        )

        print(
            "2. Ranking dos residentes"
        )

        print(
            "3. Preceptores de pacientes flamenguistas"
        )

        print(
            "4. Último atendimento de cada paciente"
        )

        print(
            "5. Percentual de alto risco por residente"
        )

        print(
            "6. Pacientes atualmente internados"
        )

        print(
            "7. Residentes sem supervisão adequada"
        )

        print(
            "8. Estatísticas mensais por unidade"
        )

        print(
            "9. Demonstrar lazy loading e eager loading"
        )

        print(
            "0. Encerrar"
        )

        opcao = input(
            "Opção: "
        ).strip()

        if opcao == "0":
            print(
                "Aplicação encerrada."
            )
            return

        acao = opcoes.get(opcao)

        if acao is None:
            print(
                "Opção inválida."
            )
            continue

        try:
            acao()

        except ValueError as erro:
            print(
                f"Dados inválidos: {erro}"
            )

        except Exception as erro:
            print(
                f"Erro durante a operação: {erro}"
            )


if __name__ == "__main__":
    main()