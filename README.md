# Sistema de Gestao Hospitalar Dra. Yuska - Etapa 1

Projeto da disciplina de Banco de Dados com SQL puro, sem ORM, conforme a Etapa 1 da especificacao.

## Tecnologia usada

- PostgreSQL 14 ou superior
- SQL puro executado via `psql`

## Estrutura

```text
sgh_dra_yuska_etapa1/
├── sql/
│   ├── 01_schema.sql                # Cria tabelas, PKs, FKs, CHECKs, UNIQUEs e indices
│   ├── 02_seed.sql                  # Insere dados de teste
│   ├── 03_crud_consultas.sql        # CRUD e consultas basicas exigidas
│   ├── 04_consultas_analiticas.sql  # Consultas analiticas exigidas
│   └── 05_all.sql                   # Executa todos os scripts em sequencia
├── docs/
│   ├── DER_SGH_Dra_Yuska.pdf        # DER em PDF
│   └── MODELAGEM_E_NORMALIZACAO.md  # Justificativas de cardinalidade e 3FN
├── diagrams/
│   └── der.dot                      # Fonte Graphviz do DER
└── README.md
```

## Como executar

### 1. Criar o banco

```bash
createdb sgh_dra_yuska
```

### 2. Executar schema e dados de teste

A partir da pasta raiz do projeto:

```bash
psql -d sgh_dra_yuska -f sql/01_schema.sql
psql -d sgh_dra_yuska -f sql/02_seed.sql
```

### 3. Executar CRUD e consultas

```bash
psql -d sgh_dra_yuska -f sql/03_crud_consultas.sql
psql -d sgh_dra_yuska -f sql/04_consultas_analiticas.sql
```

Tambem e possivel executar tudo de uma vez:

```bash
psql -d sgh_dra_yuska -f sql/05_all.sql
```

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

### Banco de dados

- CREATE TABLE com PK, FK, UNIQUE, NOT NULL e CHECK
- Dados de teste suficientes para demonstracao

### CRUD e consultas basicas

- Inserir novo atendimento verificando paciente, residente e preceptor
- Listar atendimentos de paciente especifico por data
- Listar procedimentos de um atendimento
- Atualizar endereco e convenio de paciente
- Remover procedimento realizado apenas quando `faturado = false`
- Calcular duracao media de atendimentos por residente

### Consultas analiticas

- Ranking de residentes por numero de atendimentos
- Preceptores com mais de 5 supervisoes no mes
- Plantoes escalados por unidade e residente
- Pacientes que nunca fizeram procedimento de risco ALTO

## Observacao importante

Alguns campos foram acrescentados para cumprir todos os requisitos da Etapa 1:

- `paciente.endereco`, porque o CRUD pede atualizar endereco ou convenio.
- `procedimento.nivel_risco`, porque uma consulta pede procedimentos de risco ALTO.
- `procedimento_realizado.faturado`, porque a remocao depende de nao haver faturamento associado.
