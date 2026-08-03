/*
Funções de trigger e triggers da Etapa 2.
*/


/* ============================================================
   1. Impede sobreposição de escala
   ============================================================ */

CREATE OR REPLACE FUNCTION fn_check_sobreposicao_escala()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (
        SELECT 1

        FROM escala e

        WHERE e.id_residente = NEW.id_residente
          AND e.data_plantao = NEW.data_plantao
          AND e.turno = NEW.turno
          AND e.id_escala <> COALESCE(
              NEW.id_escala,
              -1
          )
    ) THEN
        RAISE EXCEPTION
            'O residente % já possui escala em % no turno %.',
            NEW.id_residente,
            NEW.data_plantao,
            NEW.turno;
    END IF;

    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS
    trg_check_sobreposicao_escala
    ON escala;

CREATE TRIGGER trg_check_sobreposicao_escala
BEFORE INSERT OR UPDATE
ON escala
FOR EACH ROW
EXECUTE FUNCTION fn_check_sobreposicao_escala();


/* ============================================================
   2. Registra auditoria de atendimento
   ============================================================ */

CREATE OR REPLACE FUNCTION fn_audita_atendimento()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO auditoria_atendimento (
        id_atendimento,
        operacao,
        usuario,
        data_hora,
        dados_antigos,
        dados_novos
    )
    VALUES (
        CASE
            WHEN TG_OP = 'DELETE'
                THEN OLD.id_atendimento
            ELSE NEW.id_atendimento
        END,

        TG_OP,
        CURRENT_USER,
        CURRENT_TIMESTAMP,

        CASE
            WHEN TG_OP IN ('UPDATE', 'DELETE')
                THEN TO_JSONB(OLD)
            ELSE NULL
        END,

        CASE
            WHEN TG_OP IN ('INSERT', 'UPDATE')
                THEN TO_JSONB(NEW)
            ELSE NULL
        END
    );

    IF TG_OP = 'DELETE' THEN
        RETURN OLD;
    END IF;

    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS
    trg_audita_atendimento
    ON atendimento;

CREATE TRIGGER trg_audita_atendimento
AFTER INSERT OR UPDATE OR DELETE
ON atendimento
FOR EACH ROW
EXECUTE FUNCTION fn_audita_atendimento();


/* ============================================================
   3. Atualiza a média dos procedimentos
   ============================================================ */

CREATE OR REPLACE FUNCTION fn_atualiza_media_procedimentos()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE procedimento p
    SET media_tempo_procedimento = (
        SELECT
            ROUND(
                AVG(pr.tempo_real_minutos)::NUMERIC,
                2
            )

        FROM procedimento_realizado pr

        WHERE pr.id_procedimento =
              NEW.id_procedimento
    )
    WHERE p.id_procedimento =
          NEW.id_procedimento;

    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS
    trg_atualiza_media_procedimentos
    ON procedimento_realizado;

CREATE TRIGGER trg_atualiza_media_procedimentos
AFTER INSERT
ON procedimento_realizado
FOR EACH ROW
EXECUTE FUNCTION fn_atualiza_media_procedimentos();