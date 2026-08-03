from __future__ import annotations

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from hospital_yuska.modelos import Escala, Residente


def criar_escala_com_bloqueio(
    sessao: Session,
    *,
    id_unidade: int,
    data_plantao: date,
    dia_semana: str,
    turno: str,
    id_residente: int,
    id_preceptor: int,
) -> Escala:
    """
    Bloqueia a linha do residente antes de consultar e inserir a escala.

    O bloqueio pessimista impede que duas transações concluam uma escala
    conflitante para o mesmo residente.
    """

    residente = sessao.scalar(
        select(Residente)
        .where(
            Residente.id_profissional ==
            id_residente
        )
        .with_for_update()
    )

    if residente is None:
        raise ValueError(
            f"Residente {id_residente} não encontrado."
        )

    conflito = sessao.scalar(
        select(Escala.id_escala)

        .where(
            Escala.id_residente ==
            id_residente,

            Escala.data_plantao ==
            data_plantao,

            Escala.turno ==
            turno,
        )
    )

    if conflito is not None:
        raise ValueError(
            "O residente já possui escala nessa data e turno."
        )

    escala = Escala(
        id_unidade=id_unidade,
        data_plantao=data_plantao,
        dia_semana=dia_semana,
        turno=turno,
        id_residente=id_residente,
        id_preceptor=id_preceptor,
        supervisao_ativa=True,
    )

    sessao.add(escala)
    sessao.flush()

    return escala