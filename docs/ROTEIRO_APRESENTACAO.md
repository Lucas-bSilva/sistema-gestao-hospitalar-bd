# Roteiro de apresentação — Etapa 1

## Preparação

Executar no pgAdmin:

1. `sql/01_estrutura.sql`
2. `sql/02_dados_teste.sql`
3. `sql/06_validacoes.sql`

## Localização dos requisitos

| Funcionalidade | Arquivo |
|---|---|
| Estrutura, PK, FK e constraints | `sql/01_estrutura.sql` |
| Dados de teste | `sql/02_dados_teste.sql` |
| CRUD e consultas básicas | `sql/03_crud_consultas.sql` |
| Consultas analíticas | `sql/04_consultas_analiticas.sql` |
| Conferências | `sql/06_validacoes.sql` |
| Testes com rollback | `sql/07_testes_funcionais.sql` |

## Demonstração

1. Mostrar o DER.
2. Explicar as especializações.
3. Validar a carga mínima.
4. Executar os seis blocos de CRUD.
5. Executar as quatro consultas analíticas.
6. Mostrar um teste com `ROLLBACK`.
7. Explicar a normalização até a 3FN.

## Reinício do banco

Para repetir a demonstração:

1. executar `01_estrutura.sql`;
2. executar `02_dados_teste.sql`;
3. executar `06_validacoes.sql`.