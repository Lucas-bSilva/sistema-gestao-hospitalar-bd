from sqlalchemy import text

from hospital_yuska.banco import motor


def main() -> None:
    with motor.connect() as conexao:
        banco = conexao.scalar(text("SELECT current_database()"))
        versao = conexao.scalar(text("SELECT version()"))

    print(f"Conexão realizada com o banco: {banco}")
    print(versao)


if __name__ == "__main__":
    main()