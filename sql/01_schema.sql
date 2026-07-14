/*
Sistema de Gestao Hospitalar Dra. Yuska - Etapa 1
PostgreSQL 14+

Este script recria a estrutura do banco para testes da Etapa 1.
A ordem dos DROP respeita as dependencias entre as tabelas.
*/

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

/*
Tabela base da especializacao.
Dados comuns de pacientes e profissionais ficam aqui para evitar repeticao.
*/

CREATE TABLE pessoa (
    id_pessoa          BIGSERIAL PRIMARY KEY,
    nome               VARCHAR(120) NOT NULL,
    cpf                CHAR(11) NOT NULL UNIQUE,
    data_nascimento    DATE NOT NULL,
    is_flamengo        BOOLEAN NOT NULL DEFAULT FALSE,
    telefone           VARCHAR(20) NOT NULL,
    CONSTRAINT ck_pessoa_cpf_digitos CHECK (cpf ~ '^[0-9]{11}$')
);

/*
Especializacao de pessoa para pacientes atendidos pelo hospital.
O campo endereco foi incluido porque o CRUD solicitado permite atualizar endereco ou convenio.
*/
CREATE TABLE paciente (
    id_pessoa          BIGINT PRIMARY KEY REFERENCES pessoa(id_pessoa) ON DELETE CASCADE,
    num_convenio       VARCHAR(40) UNIQUE,
    alergias           TEXT,
    grupo_sanguineo    VARCHAR(3) NOT NULL,
    endereco           VARCHAR(180),
    CONSTRAINT ck_paciente_grupo_sanguineo CHECK (grupo_sanguineo IN ('A+','A-','B+','B-','AB+','AB-','O+','O-'))
);

/*
Especializacao de pessoa para profissionais do hospital.
Residente e preceptor compartilham os dados profissionais desta tabela.
*/
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

/*
O nivel de risco foi incluido para atender a consulta analitica sobre procedimentos de risco ALTO.
*/
CREATE TABLE procedimento (
    id_procedimento        BIGSERIAL PRIMARY KEY,
    codigo                 VARCHAR(20) NOT NULL UNIQUE,
    nome                   VARCHAR(100) NOT NULL,
    tempo_medio_minutos    INTEGER NOT NULL,
    nivel_risco            VARCHAR(10) NOT NULL DEFAULT 'BAIXO',
    CONSTRAINT ck_procedimento_tempo CHECK (tempo_medio_minutos > 0),
    CONSTRAINT ck_procedimento_risco CHECK (nivel_risco IN ('BAIXO','MEDIO','ALTO'))
);

/*
Cada atendimento possui exatamente um paciente, um residente e um preceptor.
*/
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

/*
Tabela associativa entre atendimento e procedimento.
A chave composta impede repetir o mesmo procedimento no mesmo atendimento.
*/
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

-- Registra os plantões e impede escalas duplicadas para o mesmo residente

CREATE TABLE escala (
    id_escala        BIGSERIAL PRIMARY KEY,
    id_unidade       BIGINT NOT NULL
        REFERENCES unidade(id_unidade) ON DELETE RESTRICT,
    data_plantao     DATE NOT NULL,
    dia_semana       VARCHAR(10) NOT NULL,
    turno            VARCHAR(10) NOT NULL,
    id_residente     BIGINT NOT NULL
        REFERENCES residente(id_profissional) ON DELETE RESTRICT,
    id_preceptor     BIGINT NOT NULL
        REFERENCES preceptor(id_profissional) ON DELETE RESTRICT,

    CONSTRAINT ck_escala_dia
        CHECK (
            dia_semana IN (
                'segunda',
                'terca',
                'quarta',
                'quinta',
                'sexta',
                'sabado',
                'domingo'
            )
        ),

    CONSTRAINT ck_escala_data_dia_coerentes
        CHECK (
            dia_semana =
            CASE EXTRACT(ISODOW FROM data_plantao)
                WHEN 1 THEN 'segunda'
                WHEN 2 THEN 'terca'
                WHEN 3 THEN 'quarta'
                WHEN 4 THEN 'quinta'
                WHEN 5 THEN 'sexta'
                WHEN 6 THEN 'sabado'
                WHEN 7 THEN 'domingo'
            END
        ),

    CONSTRAINT ck_escala_turno
        CHECK (turno IN ('manha', 'tarde', 'noite')),

    CONSTRAINT ck_escala_res_preceptor_distintos
        CHECK (id_residente <> id_preceptor),

    CONSTRAINT uq_escala_unidade_dia_turno_residente
        UNIQUE (
            id_unidade,
            dia_semana,
            turno,
            id_residente
        ),

    CONSTRAINT uq_escala_unidade_data_turno_residente
        UNIQUE (
            id_unidade,
            data_plantao,
            turno,
            id_residente
        )
);
