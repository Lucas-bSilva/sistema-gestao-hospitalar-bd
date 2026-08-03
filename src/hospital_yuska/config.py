from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


# config.py está em: raiz/src/hospital_yuska/config.py
RAIZ_PROJETO = Path(__file__).resolve().parents[2]
ARQUIVO_ENV = RAIZ_PROJETO / ".env"

# Carrega o .env da raiz e substitui variáveis antigas do sistema.
load_dotenv(dotenv_path=ARQUIVO_ENV, override=True)


@dataclass(frozen=True, slots=True)
class ConfiguracaoBanco:
    """Configurações utilizadas para acessar o PostgreSQL."""

    url_banco: str
    exibir_sql: bool


def carregar_configuracao() -> ConfiguracaoBanco:
    """Lê e valida as configurações definidas no arquivo .env."""

    url_banco = os.getenv("DATABASE_URL", "").strip()

    if not url_banco:
        raise RuntimeError(
            "A variável DATABASE_URL não foi definida. "
            "Crie e configure o arquivo .env na raiz do projeto."
        )

    valor_exibir_sql = os.getenv("EXIBIR_SQL", "false").strip().lower()

    return ConfiguracaoBanco(
        url_banco=url_banco,
        exibir_sql=valor_exibir_sql in {"1", "true", "yes", "sim"},
    )