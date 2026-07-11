# Sistema de Gestão Hospitalar Dra. Yuska — Etapa 1

Projeto desenvolvido para a disciplina de Banco de Dados utilizando PostgreSQL e SQL puro, sem ORM.

## Tecnologias

- PostgreSQL 14 ou superior
- pgAdmin 4
- VS Code
- Git e GitHub

## Estrutura do projeto

```text
sistema-gestao-hospitalar-bd/
├── diagrams/
│   └── der.dot
├── docs/
│   ├── DER_SGH_Dra_Yuska.pdf
│   ├── MODELAGEM_E_NORMALIZACAO.md
│   └── CODIGO_COMPLETO_POR_ARQUIVO.md
├── evidencias/
│   └── checklist_etapa1.md
├── sql/
│   ├── 01_schema.sql
│   ├── 02_seed.sql
│   ├── 03_crud_consultas.sql
│   ├── 04_consultas_analiticas.sql
│   ├── 05_all.sql
│   └── 06_validacoes.sql
├── .gitignore
└── README.md

Criação do banco

No pgAdmin 4:

1. Conecte-se ao servidor PostgreSQL.
2. Crie um banco chamado hospital_yuska.
3. Abra o Query Tool desse banco.


## Execução pelo pgAdmin 4

1. Abrir o pgAdmin 4.
2. Criar um banco chamado hospital_yuska.
3. Clicar com o botão direito no banco e abrir o `Query Tool`.
4. Executar os scripts nesta ordem:

```text
1. sql/01_schema.sql
2. sql/02_seed.sql
3. sql/06_validacoes.sql
4. sql/03_crud_consultas.sql
5. sql/04_consultas_analiticas.sql

6. O script 01_schema.sql                  recria as tabelas.
7. O script 02_seed.sql                    insere os dados de teste.
8. O script 03_crud_consultas.sql          demonstra o CRUD.
9. O script 04_consultas_analiticas.sql    executa as consultas analíticas.
10. script 06_validacoes.sql               confere quantidades mínimas e constraints.

No pgAdmin, o caminho do arquivo não é um comando SQL. Abra o arquivo pelo ícone de pasta ou copie seu conteúdo do VS Code para o Query Tool.

Execução completa pelo psql

O arquivo sql/05_all.sql foi criado para execução completa via terminal usando psql.

psql -d hospital_yuska -f sql/05_all.sql

Atenção: no pgAdmin, o arquivo 05_all.sql não é recomendado, porque os comandos \i são próprios do psql.

Como executar pelo psql

A partir da pasta raiz do projeto:

psql -d hospital_yuska -f sql/01_schema.sql
psql -d hospital_yuska -f sql/02_seed.sql
psql -d hospital_yuska -f sql/06_validacoes.sql
psql -d hospital_yuska -f sql/03_crud_consultas.sql
psql -d hospital_yuska -f sql/04_consultas_analiticas.sql


## Dados de teste

A carga inicial possui:

5 pacientes
5 residentes
5 preceptores
4 unidades
12 atendimentos
12 procedimentos realizados
6 procedimentos cadastrados

## Funcionalidades da Etapa 1 implementadas

### Modelagem

- DER em PDF
- Modelo relacional completo
- Justificativa de cardinalidades
- Normalizacao ate 3FN

### Implementação
- Chaves primárias e estrangeiras
- Restrições NOT NULL, UNIQUE e CHECK
- Integridade referencial
- Índices auxiliares
- CRUD e consultas básicas

O arquivo sql/03_crud_consultas.sql contém:

- inserção de atendimento com validação das referências;
- listagem de atendimentos por paciente;
- listagem de procedimentos por atendimento;
- atualização de endereço e convênio;
- remoção condicionada à ausência de faturamento;
- média de duração por residente.

## Consultas analíticas

O arquivo sql/04_consultas_analiticas.sql contém:

- ranking de residentes;
- preceptores com mais de cinco supervisões no mês;
- plantões por unidade e residente no mês corrente;
- pacientes sem procedimentos de risco alto.
- Campos adicionais

Alguns atributos foram incluídos para viabilizar requisitos descritos na própria especificação:

- paciente.endereco
- procedimento.nivel_risco
- procedimento_realizado.faturado
- escala.data_plantao
- Reinício dos testes

Para restaurar o banco ao estado inicial:

1. execute novamente sql/01_schema.sql;
2. execute novamente sql/02_seed.sql;
3. execute sql/06_validacoes.sql.