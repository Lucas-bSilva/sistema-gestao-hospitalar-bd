from __future__ import annotations

import logging
import sys
import threading
import time
from datetime import date, timedelta
from pathlib import Path

from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from hospital_yuska.banco import motor
from hospital_yuska.concorrencia.escala import (
    criar_escala_com_bloqueio,
)
from hospital_yuska.modelos import Escala


# Define caminhos absolutos a partir da raiz do projeto.
RAIZ_PROJETO = Path(__file__).resolve().parents[1]

ARQUIVO_LOG = (
    RAIZ_PROJETO
    / "evidencias"
    / "etapa2"
    / "log_concorrencia.txt"
)

ARQUIVO_LOG.parent.mkdir(
    parents=True,
    exist_ok=True,
)


def configurar_fluxos_utf8() -> None:
    """Padroniza a saída textual do processo em UTF-8."""

    for fluxo in (sys.stdout, sys.stderr):
        if fluxo is None:
            continue

        reconfigurar = getattr(
            fluxo,
            "reconfigure",
            None,
        )

        if callable(reconfigurar):
            reconfigurar(
                encoding="utf-8",
                errors="strict",
            )


configurar_fluxos_utf8()


logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(threadName)s | "
        "%(message)s"
    ),
    handlers=[
        logging.FileHandler(
            ARQUIVO_LOG,
            mode="w",
            encoding="utf-8",
            errors="strict",
        ),
        logging.StreamHandler(
            sys.stdout
        ),
    ],
    force=True,
)


# Os valores permanecem sem acentos para corresponder
# às regras já utilizadas pelo modelo do banco.
NOMES_DIAS = {
    0: "segunda",
    1: "terca",
    2: "quarta",
    3: "quinta",
    4: "sexta",
    5: "sabado",
    6: "domingo",
}


def executar_transacao(
    data_plantao: date,
    aguardar_apos_bloqueio: int,
    sinal_bloqueio: threading.Event | None = None,
) -> None:
    """Executa uma tentativa transacional de criação de escala."""

    try:
        with Session(motor) as sessao:
            with sessao.begin():
                logging.info(
                    "Iniciando transação."
                )

                criar_escala_com_bloqueio(
                    sessao,
                    id_unidade=1,
                    data_plantao=data_plantao,
                    dia_semana=NOMES_DIAS[
                        data_plantao.weekday()
                    ],
                    turno="manha",
                    id_residente=6,
                    id_preceptor=11,
                )

                logging.info(
                    "Residente bloqueado e escala preparada."
                )

                if sinal_bloqueio is not None:
                    sinal_bloqueio.set()

                if aguardar_apos_bloqueio:
                    time.sleep(
                        aguardar_apos_bloqueio
                    )

            logging.info(
                "COMMIT concluído."
            )

    except Exception as erro:
        logging.info(
            "Transação rejeitada: %s",
            erro,
        )


def main() -> None:
    """Executa duas transações concorrentes para a mesma escala."""

    data_plantao = (
        date.today()
        + timedelta(days=60)
    )

    # Remove somente o cenário anterior desta demonstração.
    with Session(motor) as sessao:
        with sessao.begin():
            sessao.execute(
                delete(Escala).where(
                    Escala.id_residente == 6,
                    Escala.data_plantao
                    == data_plantao,
                    Escala.turno == "manha",
                )
            )

    sinal_bloqueio = threading.Event()

    transacao_a = threading.Thread(
        name="Transação A",
        target=executar_transacao,
        args=(
            data_plantao,
            3,
            sinal_bloqueio,
        ),
    )

    transacao_b = threading.Thread(
        name="Transação B",
        target=executar_transacao,
        args=(
            data_plantao,
            0,
            None,
        ),
    )

    transacao_a.start()

    # A transação B começa após A adquirir o bloqueio.
    sinal_bloqueio.wait()

    transacao_b.start()

    transacao_a.join()
    transacao_b.join()

    with Session(motor) as sessao:
        total = sessao.scalar(
            select(
                func.count(
                    Escala.id_escala
                )
            ).where(
                Escala.id_residente == 6,
                Escala.data_plantao
                == data_plantao,
                Escala.turno == "manha",
            )
        )

    logging.info(
        "Total final de escalas conflitantes: %s",
        total,
    )

    caminho_relativo = ARQUIVO_LOG.relative_to(
        RAIZ_PROJETO
    )

    print(
        f"Log salvo em: {caminho_relativo}",
        flush=True,
    )


if __name__ == "__main__":
    main()