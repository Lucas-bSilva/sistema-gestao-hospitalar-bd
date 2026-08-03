/*
Evolução do modelo físico para a Etapa 2.

Este script preserva as tabelas e os dados da Etapa 1. Ele adiciona apenas
os elementos necessários às procedures, triggers, views, ORM e testes de
concorrência previstos na especificação.
*/

BEGIN;

-- A unicidade por dia da semana impedia plantões recorrentes em semanas
-- diferentes. A data do plantão passa a ser a referência operacional.
ALTER TABLE escala
    DROP CONSTRAINT IF EXISTS uq_escala_unidade_dia_turno_residente;

ALTER TABLE atendimento
    ADD COLUMN IF NOT EXISTS id_unidade BIGINT;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'fk_atendimento_unidade'
          AND conrelid = 'atendimento'::regclass
    ) THEN
        ALTER TABLE atendimento
            ADD CONSTRAINT fk_atendimento_unidade
            FOREIGN KEY (id_unidade)
            REFERENCES unidade(id_unidade)
            ON DELETE RESTRICT;
    END IF;
END;
$$;

ALTER TABLE procedimento_realizado
    ADD COLUMN IF NOT EXISTS data_hora_inicio TIMESTAMP;

ALTER TABLE procedimento
    ADD COLUMN IF NOT EXISTS media_tempo_procedimento NUMERIC(10, 2);

ALTER TABLE escala
    ADD COLUMN IF NOT EXISTS supervisao_ativa
        BOOLEAN NOT NULL DEFAULT TRUE;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'ck_procedimento_media_tempo'
          AND conrelid = 'procedimento'::regclass
    ) THEN
        ALTER TABLE procedimento
            ADD CONSTRAINT ck_procedimento_media_tempo
            CHECK (
                media_tempo_procedimento IS NULL
                OR media_tempo_procedimento > 0
            );
    END IF;
END;
$$;

-- Representa os períodos de internação dos pacientes.
CREATE TABLE IF NOT EXISTS internacao (
    id_internacao      BIGSERIAL PRIMARY KEY,

    id_paciente        BIGINT NOT NULL
        REFERENCES paciente(id_pessoa)
        ON DELETE RESTRICT,

    id_unidade         BIGINT NOT NULL
        REFERENCES unidade(id_unidade)
        ON DELETE RESTRICT,

    data_hora_entrada  TIMESTAMP NOT NULL,
    data_hora_saida    TIMESTAMP,

    CONSTRAINT ck_internacao_periodo
        CHECK (
            data_hora_saida IS NULL
            OR data_hora_saida >= data_hora_entrada
        )
);

-- Mantém o histórico das operações realizadas em atendimento.
-- id_atendimento não possui FK para preservar a auditoria após exclusões.
CREATE TABLE IF NOT EXISTS auditoria_atendimento (
    id_auditoria     BIGSERIAL PRIMARY KEY,
    id_atendimento   BIGINT,
    operacao         VARCHAR(10) NOT NULL,
    usuario          VARCHAR(120) NOT NULL,
    data_hora        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    dados_antigos    JSONB,
    dados_novos      JSONB,

    CONSTRAINT ck_auditoria_operacao
        CHECK (operacao IN ('INSERT', 'UPDATE', 'DELETE'))
);

CREATE INDEX IF NOT EXISTS ix_atendimento_unidade_data
    ON atendimento (id_unidade, data_hora);

CREATE INDEX IF NOT EXISTS ix_procedimento_realizado_inicio
    ON procedimento_realizado (
        id_atendimento,
        data_hora_inicio
    );

CREATE INDEX IF NOT EXISTS ix_internacao_paciente_entrada
    ON internacao (
        id_paciente,
        data_hora_entrada DESC
    );

CREATE INDEX IF NOT EXISTS ix_auditoria_atendimento_data
    ON auditoria_atendimento (
        id_atendimento,
        data_hora DESC
    );

-- Impede duas internações ativas simultâneas para o mesmo paciente.
CREATE UNIQUE INDEX IF NOT EXISTS uq_internacao_paciente_ativa
    ON internacao (id_paciente)
    WHERE data_hora_saida IS NULL;

-- Impede o mesmo residente de estar em duas unidades no mesmo momento.
-- O índice também protege a regra em situações de concorrência.
CREATE UNIQUE INDEX IF NOT EXISTS uq_escala_residente_data_turno
    ON escala (
        id_residente,
        data_plantao,
        turno
    );

-- Concede acesso ao usuário da aplicação, caso ele já exista.
DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM pg_roles
        WHERE rolname = 'hospital_app'
    ) THEN
        EXECUTE
            'GRANT SELECT, INSERT, UPDATE, DELETE
             ON TABLE
                atendimento,
                procedimento_realizado,
                procedimento,
                escala,
                internacao,
                auditoria_atendimento
             TO hospital_app';

        EXECUTE
            'GRANT USAGE, SELECT, UPDATE
             ON SEQUENCE
                internacao_id_internacao_seq,
                auditoria_atendimento_id_auditoria_seq
             TO hospital_app';
    END IF;
END;
$$;

COMMIT;