# Sistema de Gestão Hospitalar Dra. Yuska — Etapa 1

Projeto acadêmico desenvolvido com PostgreSQL e SQL puro, sem ORM.

## Tecnologias

- PostgreSQL 14 ou superior
- pgAdmin 4
- VS Code
- Git e GitHub

## Estrutura

```text
sistema-gestao-hospitalar-bd/
├── diagrams/
│   └── der.dot
├── docs/
│   ├── DER_SGH_Dra_Yuska.pdf
│   ├── MODELAGEM_E_NORMALIZACAO.md
│   ├── ROTEIRO_APRESENTACAO.md
│   └── CODIGO_COMPLETO_POR_ARQUIVO.md
├── evidencias/
│   └── checklist_etapa1.md
├── sql/
│   ├── 01_schema.sql
│   ├── 02_seed.sql
│   ├── 03_crud_consultas.sql
│   ├── 04_consultas_analiticas.sql
│   ├── 05_all.sql
│   ├── 06_validacoes.sql
│   └── 07_testes_funcionais.sql
├── .gitignore
└── README.md
```

## Criação do banco

No pgAdmin 4:

1. Conecte-se ao PostgreSQL;
2. Crie o banco hospital_yuska;
3. Abra o Query Tool desse banco.

## Ordem de execução no pgAdmin
```
1. sql/01_schema.sql
2. sql/02_seed.sql
3. sql/06_validacoes.sql
4. sql/03_crud_consultas.sql
5. sql/04_consultas_analiticas.sql
```
O arquivo `sql/07_testes_funcionais.sql` pode ser usado depois da
carga inicial para testar as operações sem alterar permanentemente os dados.

No pgAdmin, abra o conteúdo do arquivo pelo ícone de pasta ou copie-o
do VS Code para o Query Tool. O caminho do arquivo, sozinho, não é SQL.

## Execução completa pelo psql
```
psql -d hospital_yuska -f sql/05_all.sql
```
Os comandos `\i` do `05_all.sql` são próprios do `psql`.

## Carga de teste

- 5 pacientes
- 5 residentes
- 5 preceptores
- 4 unidades
- 12 atendimentos
- 12 procedimentos realizados
- 6 procedimentos cadastrados

## Arquivos por requisito

| Requisito | Arquivo |
| :--- | :--- |
| Estrutura e constraints | `sql/01_schema.sql` |
| Dados iniciais | `sql/02_seed.sql` |
| CRUD e consultas básicas | `sql/03_crud_consultas.sql` |
| Consultas analíticas | `sql/04_consultas_analiticas.sql` |
| Validações | `sql/06_validacoes.sql` |
| Testes repetíveis | `sql/07_testes_funcionais.sql` |
| DER | `docs/DER_SGH_Dra_Yuska.pdf` |
| Normalização | `docs/MODELAGEM_E_NORMALIZACAO.md` |

## Campos complementares

Foram adicionados campos necessários para requisitos que aparecem
nas funcionalidades da Etapa 1:

- paciente.endereco;
- procedimento.nivel_risco;
- procedimento_realizado.faturado;
- escala.data_plantao.

## Restaurar a carga inicial
```
Execute sql/01_schema.sql.
Execute sql/02_seed.sql.
Execute sql/06_validacoes.sql.
```