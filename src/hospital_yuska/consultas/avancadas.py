from __future__ import annotations

from sqlalchemy import Numeric, case, cast, func, select
from sqlalchemy.orm import Session, aliased, joinedload, selectinload

from hospital_yuska.modelos import (
    Atendimento,
    Paciente,
    Pessoa,
    Preceptor,
    Procedimento,
    ProcedimentoRealizado,
    Profissional,
    Residente,
)


def listar_preceptores_de_pacientes_flamenguistas(
    sessao: Session,
):
    """Lista preceptores que atenderam pacientes flamenguistas."""

    pessoa_preceptor = aliased(Pessoa)

    comando = (
        select(
            Preceptor.id_profissional.label(
                "id_preceptor"
            ),

            pessoa_preceptor.nome.label(
                "preceptor"
            ),
        )

        .join(
            pessoa_preceptor,

            pessoa_preceptor.id_pessoa ==
            Preceptor.id_profissional,
        )

        .join(
            Atendimento,

            Atendimento.id_preceptor ==
            Preceptor.id_profissional,
        )

        .join(
            Paciente,

            Paciente.id_pessoa ==
            Atendimento.id_paciente,
        )

        .join(
            Pessoa,

            Pessoa.id_pessoa ==
            Paciente.id_pessoa,
        )

        .where(
            Pessoa.is_flamengo.is_(True)
        )

        .distinct()

        .order_by(
            pessoa_preceptor.nome
        )
    )

    return sessao.execute(comando).all()


def ultimo_atendimento_de_cada_paciente(
    sessao: Session,
) -> list[Atendimento]:
    """Retorna o atendimento mais recente de cada paciente."""

    ordem = (
        func.row_number()
        .over(
            partition_by=
                Atendimento.id_paciente,

            order_by=(
                Atendimento.data_hora.desc(),
                Atendimento.id_atendimento.desc(),
            ),
        )
        .label("ordem")
    )

    classificados = (
        select(
            Atendimento.id_atendimento.label(
                "id_atendimento"
            ),

            ordem,
        )
        .subquery()
    )

    comando = (
        select(Atendimento)

        .join(
            classificados,

            classificados.c.id_atendimento ==
            Atendimento.id_atendimento,
        )

        .where(
            classificados.c.ordem == 1
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

            selectinload(
                Atendimento.procedimentos_realizados
            ).joinedload(
                ProcedimentoRealizado.procedimento
            ),
        )

        .order_by(
            Atendimento.id_paciente
        )
    )

    return list(
        sessao.scalars(comando).unique()
    )


def percentual_alto_risco_por_residente(
    sessao: Session,
):
    """Calcula o percentual de procedimentos de alto risco."""

    total_procedimentos = func.coalesce(
        func.sum(
            ProcedimentoRealizado.quantidade
        ),
        0,
    )

    procedimentos_alto_risco = func.coalesce(
        func.sum(
            case(
                (
                    Procedimento.nivel_risco == "ALTO",

                    ProcedimentoRealizado.quantidade,
                ),
                else_=0,
            )
        ),
        0,
    )

    percentual = case(
        (
            total_procedimentos == 0,
            0,
        ),

        else_=cast(
            procedimentos_alto_risco
            * 100.0
            / total_procedimentos,

            Numeric(10, 2),
        ),
    )

    comando = (
        select(
            Residente.id_profissional.label(
                "id_residente"
            ),

            Pessoa.nome.label(
                "residente"
            ),

            total_procedimentos.label(
                "total_procedimentos"
            ),

            procedimentos_alto_risco.label(
                "procedimentos_alto_risco"
            ),

            percentual.label(
                "percentual_alto_risco"
            ),
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

        .outerjoin(
            ProcedimentoRealizado,

            ProcedimentoRealizado.id_atendimento ==
            Atendimento.id_atendimento,
        )

        .outerjoin(
            Procedimento,

            Procedimento.id_procedimento ==
            ProcedimentoRealizado.id_procedimento,
        )

        .group_by(
            Residente.id_profissional,
            Pessoa.nome,
        )

        .order_by(
            Pessoa.nome
        )
    )

    return sessao.execute(comando).all()


def obter_atendimento_lazy(
    sessao: Session,
    id_atendimento: int,
) -> Atendimento | None:
    """Carrega relações apenas quando forem acessadas."""

    return sessao.get(
        Atendimento,
        id_atendimento,
    )


def obter_atendimento_eager(
    sessao: Session,
    id_atendimento: int,
) -> Atendimento | None:
    """Carrega atendimento e relacionamentos antecipadamente."""

    comando = (
        select(Atendimento)

        .where(
            Atendimento.id_atendimento ==
            id_atendimento
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

            selectinload(
                Atendimento.procedimentos_realizados
            ).joinedload(
                ProcedimentoRealizado.procedimento
            ),
        )
    )

    return (
        sessao
        .scalars(comando)
        .unique()
        .one_or_none()
    )