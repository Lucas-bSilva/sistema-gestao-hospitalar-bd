from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from hospital_yuska.config import carregar_configuracao

configuracao = carregar_configuracao()

motor = create_engine(
    configuracao.url_banco,
    echo=configuracao.exibir_sql,
    pool_pre_ping=True,
)

FabricaSessao = sessionmaker(
    bind=motor,
    class_=Session,
    expire_on_commit=False,
)


@contextmanager
def sessao_transacional() -> Iterator[Session]:
    sessao = FabricaSessao()

    try:
        with sessao.begin():
            yield sessao
    except Exception:
        sessao.rollback()
        raise
    finally:
        sessao.close()