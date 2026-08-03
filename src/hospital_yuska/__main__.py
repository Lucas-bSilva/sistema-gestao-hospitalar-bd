from __future__ import annotations

import argparse


def main() -> None:
    analisador = argparse.ArgumentParser(
        description=(
            "Sistema de Gestão Hospitalar "
            "Dra. Yuska — Etapa 2"
        )
    )

    analisador.add_argument(
        "--cli",
        action="store_true",
        help="abre a interface de terminal",
    )

    argumentos = analisador.parse_args()

    if argumentos.cli:
        from hospital_yuska.cli import main as iniciar_cli

        iniciar_cli()
        return

    from hospital_yuska.interface.desktop import (
        main as iniciar_desktop,
    )

    iniciar_desktop()


if __name__ == "__main__":
    main()