# Sistema de Gestao Hospitalar Dra. Yuska - Etapa 1

Projeto da disciplina de Banco de Dados com SQL puro, sem ORM, conforme a Etapa 1 da especificacao.

## Tecnologia usada

- PostgreSQL 14 ou superior
- SQL puro executado via `psql`

## Estrutura

```text
sistema-gestao-hospitalar-bd/
├── sql/
│   ├── 01_schema.sql                # Cria tabelas, chaves, restricoes e indices
│   ├── 02_seed.sql                  # Insere os dados de teste
│   ├── 03_crud_consultas.sql        # Operacoes CRUD e consultas basicas
│   ├── 04_consultas_analiticas.sql  # Consultas analiticas da Etapa 1
│   ├── 05_all.sql                   # Execucao completa pelo psql
│   └── 06_validacoes.sql            # Conferencias de dados e restricoes
├── docs/
│   ├── DER_SGH_Dra_Yuska.pdf
│   ├── MODELAGEM_E_NORMALIZACAO.md
│   └── CODIGO_COMPLETO_POR_ARQUIVO.md
├── diagrams/
│   └── der.dot
└── README.md
```

## Execução pelo pgAdmin 4

1. Abrir o pgAdmin 4.
2. Criar um banco chamado `hospital_yuska`.
3. Clicar com o botão direito no banco e abrir o `Query Tool`.
4. Executar os scripts nesta ordem:

```text
1. sql/01_schema.sql
2. sql/02_seed.sql
3. sql/06_validacoes.sql
4. sql/03_crud_consultas.sql
5. sql/04_consultas_analiticas.sql

6. O script 01_schema.sql recria as tabelas.
7. O script 02_seed.sql insere os dados de teste.
8. O script 03_crud_consultas.sql demonstra o CRUD.
9. O script 04_consultas_analiticas.sql executa as consultas analíticas.
10. script 06_validacoes.sql confere quantidades mínimas e constraints.

No pgAdmin, recomenda-se abrir cada arquivo no VS Code, copiar o conteúdo, colar no Query Tool e executar.

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


## Dados minimos atendidos

- 5 pacientes
- 5 residentes
- 5 preceptores
- 4 unidades
- 12 atendimentos
- 12 procedimentos realizados
- 6 procedimentos cadastrados

## Funcionalidades da Etapa 1 implementadas

### Modelagem

- DER em PDF
- Modelo relacional completo
- Justificativa de cardinalidades
- Evidencia de normalizacao ate 3FN

### Implementação do Banco

- Tabelas com PRIMARY KEY
- Tabelas com FOREIGN KEY
- Restrições NOT NULL
- Restrições UNIQUE
- Restrições CHECK
- Dados de teste para validação

### Banco de dados

- CREATE TABLE com PK, FK, UNIQUE, NOT NULL e CHECK
- Dados de teste suficientes para demonstracao
- Indices auxiliares para consultas recorrentes

### CRUD e consultas basicas

Arquivo:

sql/03_crud_consultas.sql

- Inserção de novo atendimento validando paciente, residente e preceptor
- Listagem dos atendimentos de um paciente específico
- Listagem dos procedimentos realizados em um atendimento
- Atualização de endereço e convênio de paciente
- Remoção de procedimento realizado apenas se não estiver faturado
- Cálculo do tempo médio de duração dos atendimentos por residente

### Consultas analiticas

Arquivo:

sql/04_consultas_analiticas.sql

- Ranking de residentes por numero de atendimentos
- Preceptores que supervisionaram mais de 5 atendimentos em determinado mes
- Plantoes escalados por unidade e residente no mes corrente
- Pacientes que nunca realizaram procedimento de risco ALTO

### Arquivo de validação

O arquivo:

sql/06_validacoes.sql

serve para conferir rapidamente se os dados mínimos foram inseridos e se as restrições principais foram criadas.

Observações de implementação

Alguns campos foram acrescentados para atender melhor aos requisitos da Etapa 1:

paciente.endereco: usado no CRUD de atualização de paciente.
procedimento.nivel_risco: usado na consulta de pacientes sem procedimento de risco ALTO.
procedimento_realizado.faturado: usado para impedir exclusão de procedimento já faturado.
escala.data_plantao: usado para consultar plantões no mês corrente.


### Alguns campos foram acrescentados para atender diretamente aos requisitos da Etapa 1:

paciente.endereco: necessario para o requisito de atualizar endereco ou convenio.
procedimento.nivel_risco: necessario para consultar pacientes sem procedimento de risco ALTO.
procedimento_realizado.faturado: necessario para impedir exclusao de procedimento ja faturado.
escala.data_plantao: necessario para filtrar plantoes do mes corrente.
