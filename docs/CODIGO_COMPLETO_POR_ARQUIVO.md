# Codigo completo por arquivo

## README.md

```
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

```

## docs/MODELAGEM_E_NORMALIZACAO.md

```
# Modelagem e Normalizacao - Etapa 1

## 1. Entidades principais

O projeto representa o Hospital Universitario Dra. Yuska Maritan Brito com as entidades Pessoa, Paciente, Profissional, Residente, Preceptor, Unidade, Escala, Atendimento, Procedimento e Procedimento Realizado.

## 2. Especializacao

Pessoa e uma entidade generalizada. Paciente e Profissional sao especializacoes de Pessoa, pois ambos compartilham nome, CPF, data de nascimento, indicador `is_flamengo` e telefone.

Profissional tambem e especializado em Residente e Preceptor. A especificacao informa que um profissional pode atuar como preceptor em um periodo e como residente em outro, mantendo historico. Na Etapa 1, o papel atual e representado pelas tabelas `residente` e `preceptor`, sempre ligadas ao mesmo identificador de `profissional`.

## 3. Cardinalidades

- Pessoa 1:0..1 Paciente: nem toda pessoa precisa ser paciente, mas todo paciente e uma pessoa.
- Pessoa 1:0..1 Profissional: nem toda pessoa precisa ser profissional, mas todo profissional e uma pessoa.
- Profissional 1:0..1 Residente e Profissional 1:0..1 Preceptor: o papel atual do profissional e especializado.
- Paciente 1:N Atendimento: cada atendimento possui exatamente um paciente; um paciente pode ter varios atendimentos.
- Residente 1:N Atendimento: cada atendimento tem exatamente um residente responsavel.
- Preceptor 1:N Atendimento: cada atendimento tem exatamente um preceptor supervisor.
- Atendimento N:M Procedimento, resolvido por Procedimento_Realizado: um atendimento pode ter um ou mais procedimentos, e um procedimento pode ocorrer em varios atendimentos.
- Unidade 1:N Escala: cada escala pertence a uma unidade, e uma unidade possui varias escalas.
- Residente 1:N Escala e Preceptor 1:N Escala: cada plantao registra um residente e um preceptor.

## 4. Modelo relacional

- PESSOA(id_pessoa PK, nome, cpf UNIQUE, data_nascimento, is_flamengo, telefone)
- PACIENTE(id_pessoa PK/FK, num_convenio UNIQUE, alergias, grupo_sanguineo, endereco)
- PROFISSIONAL(id_pessoa PK/FK, crm UNIQUE, data_admissao, especialidade)
- RESIDENTE(id_profissional PK/FK, ano_residencia)
- PRECEPTOR(id_profissional PK/FK, titulacao)
- UNIDADE(id_unidade PK, nome UNIQUE, tipo, capacidade_leitos)
- PROCEDIMENTO(id_procedimento PK, codigo UNIQUE, nome, tempo_medio_minutos, nivel_risco)
- ATENDIMENTO(id_atendimento PK, data_hora, duracao_minutos, id_paciente FK, id_residente FK, id_preceptor FK)
- PROCEDIMENTO_REALIZADO(id_atendimento PK/FK, id_procedimento PK/FK, quantidade, tempo_real_minutos, observacao, faturado)
- ESCALA(id_escala PK, id_unidade FK, dia_semana, turno, id_residente FK, id_preceptor FK, UNIQUE(id_unidade, dia_semana, turno, id_residente))

## 5. Evidencia de 3FN

O modelo esta em 1FN porque todos os atributos sao atomicos. Atributos multivalorados, como procedimentos dentro de um atendimento, foram separados em `procedimento_realizado`.

O modelo esta em 2FN porque as tabelas com chave composta, especialmente `procedimento_realizado`, possuem atributos dependentes da chave completa `(id_atendimento, id_procedimento)`, e nao apenas de parte dela.

O modelo esta em 3FN porque nao ha dependencia transitiva relevante entre atributos nao chave. Dados de pessoa ficam em `pessoa`; dados especificos de paciente ficam em `paciente`; dados de procedimento ficam em `procedimento`; dados do atendimento ficam em `atendimento`. Assim, por exemplo, o nome do residente nao e repetido em `atendimento`, apenas sua FK.

## 6. Observacoes de adequacao a especificacao

A especificacao da Etapa 1 menciona atualizar endereco ou convenio do paciente, embora o diagrama textual inicial liste apenas numero do convenio, alergias e grupo sanguineo. Para atender ao CRUD solicitado, foi acrescentado o campo `endereco` em `paciente`.

A consulta de pacientes sem procedimento de risco alto exige a classificacao de risco do procedimento. Por isso, foi acrescentado `nivel_risco` em `procedimento`, com CHECK para BAIXO, MEDIO e ALTO.

A remocao de procedimento realizado depende de verificar faturamento. Por isso, foi acrescentado o campo booleano `faturado` em `procedimento_realizado`.

```

## diagrams/der.dot

```
digraph DER {
  graph [rankdir=LR, bgcolor="white", splines=ortho, nodesep=0.6, ranksep=1.0];
  node [shape=record, fontname="Arial", fontsize=10];
  edge [fontname="Arial", fontsize=9];

  PESSOA [label="{PESSOA|PK id_pessoa\lnome\lCPF UNIQUE\ldata_nascimento\lis_flamengo\ltelefone\l}"];
  PACIENTE [label="{PACIENTE|PK/FK id_pessoa\lnum_convenio UNIQUE\lalergias\lgrupo_sanguineo\lendereco\l}"];
  PROFISSIONAL [label="{PROFISSIONAL|PK/FK id_pessoa\lCRM UNIQUE\ldata_admissao\lespecialidade\l}"];
  RESIDENTE [label="{RESIDENTE|PK/FK id_profissional\lano_residencia\l}"];
  PRECEPTOR [label="{PRECEPTOR|PK/FK id_profissional\ltitulacao\l}"];
  ATENDIMENTO [label="{ATENDIMENTO|PK id_atendimento\ldata_hora\lduracao_minutos\lFK id_paciente\lFK id_residente\lFK id_preceptor\l}"];
  PROCEDIMENTO [label="{PROCEDIMENTO|PK id_procedimento\lcodigo UNIQUE\lnome\ltempo_medio_minutos\lnivel_risco\l}"];
  PROCEDIMENTO_REALIZADO [label="{PROCEDIMENTO_REALIZADO|PK/FK id_atendimento\lPK/FK id_procedimento\lquantidade\ltempo_real_minutos\lobservacao\lfaturado\l}"];
  UNIDADE [label="{UNIDADE|PK id_unidade\lnome UNIQUE\ltipo\lcapacidade_leitos\l}"];
  ESCALA [label="{ESCALA|PK id_escala\lFK id_unidade\ldia_semana\lturno\lFK id_residente\lFK id_preceptor\lUNIQUE(unidade,dia,turno,residente)\l}"];

  PESSOA -> PACIENTE [label="especializacao 1:0..1"];
  PESSOA -> PROFISSIONAL [label="especializacao 1:0..1"];
  PROFISSIONAL -> RESIDENTE [label="papel historico 1:0..1"];
  PROFISSIONAL -> PRECEPTOR [label="papel historico 1:0..1"];

  PACIENTE -> ATENDIMENTO [label="1:N"];
  RESIDENTE -> ATENDIMENTO [label="1:N realiza"];
  PRECEPTOR -> ATENDIMENTO [label="1:N supervisiona"];

  ATENDIMENTO -> PROCEDIMENTO_REALIZADO [label="1:N"];
  PROCEDIMENTO -> PROCEDIMENTO_REALIZADO [label="1:N"];

  UNIDADE -> ESCALA [label="1:N"];
  RESIDENTE -> ESCALA [label="1:N"];
  PRECEPTOR -> ESCALA [label="1:N"];
}

```

## sql/01_schema.sql

```
-- Sistema de Gestao Hospitalar Dra. Yuska - Etapa 1
-- PostgreSQL 14+

DROP TABLE IF EXISTS procedimento_realizado CASCADE;
DROP TABLE IF EXISTS atendimento CASCADE;
DROP TABLE IF EXISTS escala CASCADE;
DROP TABLE IF EXISTS procedimento CASCADE;
DROP TABLE IF EXISTS unidade CASCADE;
DROP TABLE IF EXISTS residente CASCADE;
DROP TABLE IF EXISTS preceptor CASCADE;
DROP TABLE IF EXISTS profissional CASCADE;
DROP TABLE IF EXISTS paciente CASCADE;
DROP TABLE IF EXISTS pessoa CASCADE;

CREATE TABLE pessoa (
    id_pessoa          BIGSERIAL PRIMARY KEY,
    nome               VARCHAR(120) NOT NULL,
    cpf                CHAR(11) NOT NULL UNIQUE,
    data_nascimento    DATE NOT NULL,
    is_flamengo        BOOLEAN NOT NULL DEFAULT FALSE,
    telefone           VARCHAR(20) NOT NULL,
    CONSTRAINT ck_pessoa_cpf_digits CHECK (cpf ~ '^[0-9]{11}$')
);

CREATE TABLE paciente (
    id_pessoa          BIGINT PRIMARY KEY REFERENCES pessoa(id_pessoa) ON DELETE CASCADE,
    num_convenio       VARCHAR(40) UNIQUE,
    alergias           TEXT,
    grupo_sanguineo    VARCHAR(3) NOT NULL,
    endereco           VARCHAR(180),
    CONSTRAINT ck_paciente_grupo_sanguineo CHECK (grupo_sanguineo IN ('A+','A-','B+','B-','AB+','AB-','O+','O-'))
);

CREATE TABLE profissional (
    id_pessoa          BIGINT PRIMARY KEY REFERENCES pessoa(id_pessoa) ON DELETE CASCADE,
    crm                VARCHAR(20) NOT NULL UNIQUE,
    data_admissao      DATE NOT NULL,
    especialidade      VARCHAR(80) NOT NULL
);

CREATE TABLE preceptor (
    id_profissional    BIGINT PRIMARY KEY REFERENCES profissional(id_pessoa) ON DELETE CASCADE,
    titulacao          VARCHAR(60) NOT NULL
);

CREATE TABLE residente (
    id_profissional    BIGINT PRIMARY KEY REFERENCES profissional(id_pessoa) ON DELETE CASCADE,
    ano_residencia     VARCHAR(2) NOT NULL,
    CONSTRAINT ck_residente_ano CHECK (ano_residencia IN ('R1','R2','R3'))
);

CREATE TABLE unidade (
    id_unidade         BIGSERIAL PRIMARY KEY,
    nome               VARCHAR(80) NOT NULL UNIQUE,
    tipo               VARCHAR(30) NOT NULL,
    capacidade_leitos  INTEGER NOT NULL,
    CONSTRAINT ck_unidade_tipo CHECK (tipo IN ('Enfermaria','UTI','Pronto-Socorro','Ambulatorio')),
    CONSTRAINT ck_unidade_capacidade CHECK (capacidade_leitos >= 0)
);

CREATE TABLE procedimento (
    id_procedimento        BIGSERIAL PRIMARY KEY,
    codigo                 VARCHAR(20) NOT NULL UNIQUE,
    nome                   VARCHAR(100) NOT NULL,
    tempo_medio_minutos    INTEGER NOT NULL,
    nivel_risco            VARCHAR(10) NOT NULL DEFAULT 'BAIXO',
    CONSTRAINT ck_procedimento_tempo CHECK (tempo_medio_minutos > 0),
    CONSTRAINT ck_procedimento_risco CHECK (nivel_risco IN ('BAIXO','MEDIO','ALTO'))
);

CREATE TABLE atendimento (
    id_atendimento     BIGSERIAL PRIMARY KEY,
    data_hora          TIMESTAMP NOT NULL,
    duracao_minutos    INTEGER NOT NULL,
    id_paciente        BIGINT NOT NULL REFERENCES paciente(id_pessoa) ON DELETE RESTRICT,
    id_residente       BIGINT NOT NULL REFERENCES residente(id_profissional) ON DELETE RESTRICT,
    id_preceptor       BIGINT NOT NULL REFERENCES preceptor(id_profissional) ON DELETE RESTRICT,
    CONSTRAINT ck_atendimento_duracao CHECK (duracao_minutos > 0),
    CONSTRAINT ck_atendimento_res_preceptor_distintos CHECK (id_residente <> id_preceptor)
);

CREATE TABLE procedimento_realizado (
    id_atendimento       BIGINT NOT NULL REFERENCES atendimento(id_atendimento) ON DELETE CASCADE,
    id_procedimento      BIGINT NOT NULL REFERENCES procedimento(id_procedimento) ON DELETE RESTRICT,
    quantidade           INTEGER NOT NULL,
    tempo_real_minutos   INTEGER NOT NULL,
    observacao           TEXT,
    faturado             BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (id_atendimento, id_procedimento),
    CONSTRAINT ck_pr_quantidade CHECK (quantidade > 0),
    CONSTRAINT ck_pr_tempo_real CHECK (tempo_real_minutos > 0)
);

CREATE TABLE escala (
    id_escala        BIGSERIAL PRIMARY KEY,
    id_unidade       BIGINT NOT NULL REFERENCES unidade(id_unidade) ON DELETE RESTRICT,
    dia_semana       VARCHAR(10) NOT NULL,
    turno            VARCHAR(10) NOT NULL,
    id_residente     BIGINT NOT NULL REFERENCES residente(id_profissional) ON DELETE RESTRICT,
    id_preceptor     BIGINT NOT NULL REFERENCES preceptor(id_profissional) ON DELETE RESTRICT,
    CONSTRAINT ck_escala_dia CHECK (dia_semana IN ('segunda','terca','quarta','quinta','sexta','sabado','domingo')),
    CONSTRAINT ck_escala_turno CHECK (turno IN ('manha','tarde','noite')),
    CONSTRAINT ck_escala_res_preceptor_distintos CHECK (id_residente <> id_preceptor),
    CONSTRAINT uq_escala_unidade_dia_turno_residente UNIQUE (id_unidade, dia_semana, turno, id_residente)
);

CREATE INDEX idx_atendimento_paciente_data ON atendimento(id_paciente, data_hora);
CREATE INDEX idx_atendimento_residente ON atendimento(id_residente);
CREATE INDEX idx_atendimento_preceptor_data ON atendimento(id_preceptor, data_hora);
CREATE INDEX idx_pr_procedimento ON procedimento_realizado(id_procedimento);
CREATE INDEX idx_escala_unidade_residente ON escala(id_unidade, id_residente);

```

## sql/02_seed.sql

```
-- Dados de teste minimos exigidos pela Etapa 1

INSERT INTO pessoa (nome, cpf, data_nascimento, is_flamengo, telefone) VALUES
('Ana Clara Souza', '11111111111', '1995-03-10', TRUE,  '81990000001'),
('Bruno Henrique Lima', '22222222222', '1988-07-22', FALSE, '81990000002'),
('Carla Mendes Rocha', '33333333333', '2001-01-15', TRUE,  '81990000003'),
('Diego Alves Martins', '44444444444', '1979-11-30', FALSE, '81990000004'),
('Elisa Fernanda Nunes', '55555555555', '1990-05-05', TRUE,  '81990000005'),
('Felipe Res R1', '66666666666', '1998-02-12', FALSE, '81990000006'),
('Gabriela Res R2', '77777777777', '1997-09-18', TRUE,  '81990000007'),
('Hugo Res R3', '88888888888', '1996-12-02', FALSE, '81990000008'),
('Isabela Res R1', '99999999991', '1999-06-20', TRUE,  '81990000009'),
('Joao Res R2', '99999999992', '1998-04-08', FALSE, '81990000010'),
('Karla Preceptora', '99999999993', '1975-08-14', FALSE, '81990000011'),
('Luiz Preceptor', '99999999994', '1970-10-11', TRUE,  '81990000012'),
('Marina Preceptora', '99999999995', '1980-03-27', FALSE, '81990000013'),
('Nestor Preceptor', '99999999996', '1968-01-09', FALSE, '81990000014'),
('Olivia Preceptora', '99999999997', '1982-12-19', TRUE,  '81990000015');

INSERT INTO paciente (id_pessoa, num_convenio, alergias, grupo_sanguineo, endereco) VALUES
(1, 'CONV-001', 'Dipirona', 'A+',  'Rua A, 100'),
(2, 'CONV-002', 'Nenhuma',  'O+',  'Rua B, 200'),
(3, 'CONV-003', 'Penicilina','B-',  'Rua C, 300'),
(4, 'CONV-004', 'Latex',    'AB+', 'Rua D, 400'),
(5, 'CONV-005', 'Nenhuma',  'O-',  'Rua E, 500');

INSERT INTO profissional (id_pessoa, crm, data_admissao, especialidade) VALUES
(6,  'CRM-PE-1001', '2024-02-01', 'Clinica Medica'),
(7,  'CRM-PE-1002', '2023-02-01', 'Pediatria'),
(8,  'CRM-PE-1003', '2022-02-01', 'Cirurgia Geral'),
(9,  'CRM-PE-1004', '2024-02-01', 'Urgencia'),
(10, 'CRM-PE-1005', '2023-02-01', 'Clinica Medica'),
(11, 'CRM-PE-2001', '2010-01-15', 'Clinica Medica'),
(12, 'CRM-PE-2002', '2008-03-20', 'Cirurgia Geral'),
(13, 'CRM-PE-2003', '2015-07-01', 'Pediatria'),
(14, 'CRM-PE-2004', '2005-05-10', 'UTI'),
(15, 'CRM-PE-2005', '2012-09-17', 'Urgencia');

INSERT INTO residente (id_profissional, ano_residencia) VALUES
(6, 'R1'), (7, 'R2'), (8, 'R3'), (9, 'R1'), (10, 'R2');

INSERT INTO preceptor (id_profissional, titulacao) VALUES
(11, 'doutor'), (12, 'mestre'), (13, 'doutor'), (14, 'especialista'), (15, 'doutor');

INSERT INTO unidade (nome, tipo, capacidade_leitos) VALUES
('Enfermaria Geral', 'Enfermaria', 40),
('UTI Adulto', 'UTI', 12),
('Pronto-Socorro Central', 'Pronto-Socorro', 20),
('Ambulatorio Escola', 'Ambulatorio', 10);

INSERT INTO procedimento (codigo, nome, tempo_medio_minutos, nivel_risco) VALUES
('PROC-001', 'Sutura simples', 30, 'MEDIO'),
('PROC-002', 'Coleta de sangue', 10, 'BAIXO'),
('PROC-003', 'Aplicacao de medicacao', 15, 'BAIXO'),
('PROC-004', 'Drenagem de abscesso', 45, 'ALTO'),
('PROC-005', 'Curativo especial', 25, 'MEDIO'),
('PROC-006', 'Intubacao orotraqueal', 20, 'ALTO');

INSERT INTO atendimento (data_hora, duracao_minutos, id_paciente, id_residente, id_preceptor) VALUES
('2026-06-01 08:30', 50, 1, 6, 11),
('2026-06-02 09:00', 35, 2, 7, 12),
('2026-06-03 14:20', 70, 3, 8, 11),
('2026-06-04 19:10', 45, 4, 9, 13),
('2026-06-05 10:15', 40, 5, 10, 14),
('2026-06-06 11:30', 55, 1, 6, 11),
('2026-06-07 15:45', 60, 2, 7, 11),
('2026-06-08 20:00', 80, 3, 8, 15),
('2026-06-09 08:00', 25, 4, 9, 13),
('2026-06-10 13:00', 65, 5, 10, 11),
('2026-06-11 09:30', 30, 1, 7, 11),
('2026-06-12 10:00', 32, 2, 6, 11);

INSERT INTO procedimento_realizado (id_atendimento, id_procedimento, quantidade, tempo_real_minutos, observacao, faturado) VALUES
(1, 1, 1, 35, 'Sutura sem intercorrencias', FALSE),
(1, 2, 1, 12, 'Coleta inicial', FALSE),
(2, 3, 1, 16, 'Medicacao administrada', FALSE),
(3, 4, 1, 50, 'Drenagem com dor local', TRUE),
(4, 5, 2, 30, 'Curativos trocados', FALSE),
(5, 2, 1, 9,  'Coleta rapida', FALSE),
(6, 3, 2, 28, 'Duas aplicacoes', FALSE),
(7, 6, 1, 22, 'Procedimento critico estabilizado', TRUE),
(8, 4, 1, 47, 'Drenagem com sangramento leve', FALSE),
(9, 2, 1, 10, 'Coleta sem intercorrencias', FALSE),
(10, 5, 1, 25, 'Curativo planejado', FALSE),
(11, 3, 1, 14, 'Medicacao sem reacao', FALSE);

INSERT INTO escala (id_unidade, dia_semana, turno, id_residente, id_preceptor) VALUES
(1, 'segunda', 'manha', 6, 11),
(2, 'segunda', 'tarde', 7, 12),
(3, 'terca', 'noite', 8, 13),
(4, 'quarta', 'manha', 9, 14),
(1, 'quinta', 'tarde', 10, 15),
(2, 'sexta', 'noite', 6, 11),
(3, 'sabado', 'manha', 7, 13),
(4, 'domingo', 'tarde', 8, 15);

```

## sql/03_crud_consultas.sql

```
-- CRUD e consultas basicas - SQL puro

-- 1) Inserir novo atendimento verificando se paciente, residente e preceptor existem.
-- Troque os valores do WITH parametros conforme a necessidade.
WITH parametros AS (
    SELECT
        TIMESTAMP '2026-06-20 09:00' AS data_hora,
        45 AS duracao_minutos,
        1::BIGINT AS id_paciente,
        6::BIGINT AS id_residente,
        11::BIGINT AS id_preceptor
), validacao AS (
    SELECT p.*
    FROM parametros p
    WHERE EXISTS (SELECT 1 FROM paciente WHERE id_pessoa = p.id_paciente)
      AND EXISTS (SELECT 1 FROM residente WHERE id_profissional = p.id_residente)
      AND EXISTS (SELECT 1 FROM preceptor WHERE id_profissional = p.id_preceptor)
)
INSERT INTO atendimento (data_hora, duracao_minutos, id_paciente, id_residente, id_preceptor)
SELECT data_hora, duracao_minutos, id_paciente, id_residente, id_preceptor
FROM validacao
RETURNING *;

-- 2) Listar todos os atendimentos de um paciente especifico, ordenados por data.
SELECT
    a.id_atendimento,
    a.data_hora,
    a.duracao_minutos,
    pp.nome AS paciente,
    pr.nome AS residente,
    pc.nome AS preceptor
FROM atendimento a
JOIN pessoa pp ON pp.id_pessoa = a.id_paciente
JOIN pessoa pr ON pr.id_pessoa = a.id_residente
JOIN pessoa pc ON pc.id_pessoa = a.id_preceptor
WHERE a.id_paciente = 1
ORDER BY a.data_hora;

-- 3) Listar procedimentos realizados em um atendimento.
SELECT
    a.id_atendimento,
    proc.codigo,
    proc.nome AS procedimento,
    pr.quantidade,
    pr.tempo_real_minutos,
    pr.observacao
FROM procedimento_realizado pr
JOIN procedimento proc ON proc.id_procedimento = pr.id_procedimento
JOIN atendimento a ON a.id_atendimento = pr.id_atendimento
WHERE a.id_atendimento = 1
ORDER BY proc.nome;

-- 4) Atualizar dados de um paciente: endereco e convenio.
UPDATE paciente
SET endereco = 'Rua Atualizada, 123',
    num_convenio = 'CONV-001-ATUAL'
WHERE id_pessoa = 1
RETURNING *;

-- 5) Remover procedimento realizado apenas se ainda nao houver faturamento associado.
DELETE FROM procedimento_realizado
WHERE id_atendimento = 1
  AND id_procedimento = 2
  AND faturado = FALSE
RETURNING *;

-- 6) Calcular tempo medio de duracao dos atendimentos por residente.
SELECT
    r.id_profissional AS id_residente,
    p.nome AS residente,
    ROUND(AVG(a.duracao_minutos)::numeric, 2) AS media_duracao_minutos,
    COUNT(*) AS total_atendimentos
FROM atendimento a
JOIN residente r ON r.id_profissional = a.id_residente
JOIN pessoa p ON p.id_pessoa = r.id_profissional
GROUP BY r.id_profissional, p.nome
ORDER BY media_duracao_minutos DESC;

```

## sql/04_consultas_analiticas.sql

```
-- Consultas analiticas - SQL puro

-- 1) Ranking dos residentes por numero de atendimentos realizados.
SELECT
    DENSE_RANK() OVER (ORDER BY COUNT(a.id_atendimento) DESC) AS posicao,
    p.nome AS residente,
    COUNT(a.id_atendimento) AS total_atendimentos
FROM residente r
JOIN pessoa p ON p.id_pessoa = r.id_profissional
LEFT JOIN atendimento a ON a.id_residente = r.id_profissional
GROUP BY r.id_profissional, p.nome
ORDER BY total_atendimentos DESC, residente;

-- 2) Preceptores que supervisionaram mais de 5 atendimentos em um determinado mes.
-- Parametro exemplo: junho/2026.
SELECT
    p.nome AS preceptor,
    COUNT(*) AS total_supervisoes
FROM atendimento a
JOIN pessoa p ON p.id_pessoa = a.id_preceptor
WHERE a.data_hora >= DATE '2026-06-01'
  AND a.data_hora <  DATE '2026-07-01'
GROUP BY a.id_preceptor, p.nome
HAVING COUNT(*) > 5
ORDER BY total_supervisoes DESC;

-- 3) Para cada unidade, quantidade de plantoes escalados por residente no mes corrente.
-- Como a Etapa 1 define dia_semana/turno, e nao data do plantao, a consulta mostra
-- a quantidade de combinacoes fixas de escala por unidade e residente no cadastro atual.
SELECT
    u.nome AS unidade,
    pr.nome AS residente,
    COUNT(e.id_escala) AS quantidade_plantoes_cadastrados
FROM unidade u
LEFT JOIN escala e ON e.id_unidade = u.id_unidade
LEFT JOIN pessoa pr ON pr.id_pessoa = e.id_residente
GROUP BY u.id_unidade, u.nome, pr.nome
ORDER BY u.nome, quantidade_plantoes_cadastrados DESC, residente;

-- 4) Pacientes que nunca realizaram procedimento de nivel de risco ALTO.
SELECT
    p.id_pessoa AS id_paciente,
    p.nome AS paciente,
    pa.num_convenio
FROM paciente pa
JOIN pessoa p ON p.id_pessoa = pa.id_pessoa
WHERE NOT EXISTS (
    SELECT 1
    FROM atendimento a
    JOIN procedimento_realizado pr ON pr.id_atendimento = a.id_atendimento
    JOIN procedimento proc ON proc.id_procedimento = pr.id_procedimento
    WHERE a.id_paciente = pa.id_pessoa
      AND proc.nivel_risco = 'ALTO'
)
ORDER BY p.nome;

```

## sql/05_all.sql

```
\i sql/01_schema.sql
\i sql/02_seed.sql
\i sql/03_crud_consultas.sql
\i sql/04_consultas_analiticas.sql

```

