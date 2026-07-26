/*
Stored procedures da Etapa 2.

As procedures não executam COMMIT internamente. A atomicidade é garantida
pela transação do comando CALL ou pela transação aberta pelo chamador.
Qualquer exceção desfaz as alterações realizadas pela chamada.
*/


/* ============================================================
   1. Registra atendimento e procedimentos na mesma transação
   ============================================================ */

CREATE OR REPLACE PROCEDURE sp_registrar_atendimento_completo(
    p_data_hora         TIMESTAMP,
    p_duracao_minutos   INTEGER,
    p_id_paciente       BIGINT,
    p_id_residente      BIGINT,
    p_id_preceptor      BIGINT,
    p_id_unidade        BIGINT,
    p_procedimentos     JSONB
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_id_atendimento   BIGINT;
    v_item             JSONB;
    v_id_procedimento  BIGINT;
    v_quantidade       INTEGER;
    v_tempo_real       INTEGER;
    v_inicio           TIMESTAMP;
BEGIN
    IF p_data_hora IS NULL THEN
        RAISE EXCEPTION
            'A data e o horário do atendimento são obrigatórios.';
    END IF;

    IF p_duracao_minutos IS NULL
       OR p_duracao_minutos <= 0 THEN
        RAISE EXCEPTION
            'A duração do atendimento deve ser positiva.';
    END IF;

    IF p_id_residente = p_id_preceptor THEN
        RAISE EXCEPTION
            'Residente e preceptor devem ser profissionais distintos.';
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM paciente
        WHERE id_pessoa = p_id_paciente
    ) THEN
        RAISE EXCEPTION
            'Paciente % não encontrado.',
            p_id_paciente;
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM residente
        WHERE id_profissional = p_id_residente
    ) THEN
        RAISE EXCEPTION
            'Residente % não encontrado.',
            p_id_residente;
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM preceptor
        WHERE id_profissional = p_id_preceptor
    ) THEN
        RAISE EXCEPTION
            'Preceptor % não encontrado.',
            p_id_preceptor;
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM unidade
        WHERE id_unidade = p_id_unidade
    ) THEN
        RAISE EXCEPTION
            'Unidade % não encontrada.',
            p_id_unidade;
    END IF;

    IF p_procedimentos IS NULL
       OR JSONB_TYPEOF(p_procedimentos) <> 'array'
       OR JSONB_ARRAY_LENGTH(p_procedimentos) = 0 THEN
        RAISE EXCEPTION
            'Informe ao menos um procedimento em um array JSON.';
    END IF;

    INSERT INTO atendimento (
        data_hora,
        duracao_minutos,
        id_paciente,
        id_residente,
        id_preceptor,
        id_unidade
    )
    VALUES (
        p_data_hora,
        p_duracao_minutos,
        p_id_paciente,
        p_id_residente,
        p_id_preceptor,
        p_id_unidade
    )
    RETURNING id_atendimento
    INTO v_id_atendimento;

    FOR v_item IN
        SELECT valor
        FROM JSONB_ARRAY_ELEMENTS(p_procedimentos)
            AS itens(valor)
    LOOP
        v_id_procedimento := NULLIF(
            v_item ->> 'id_procedimento',
            ''
        )::BIGINT;

        v_quantidade := NULLIF(
            v_item ->> 'quantidade',
            ''
        )::INTEGER;

        v_tempo_real := NULLIF(
            v_item ->> 'tempo_real_minutos',
            ''
        )::INTEGER;

        v_inicio := COALESCE(
            NULLIF(
                v_item ->> 'data_hora_inicio',
                ''
            )::TIMESTAMP,
            p_data_hora
        );

        IF v_id_procedimento IS NULL
           OR v_quantidade IS NULL
           OR v_tempo_real IS NULL THEN
            RAISE EXCEPTION
                'Cada item deve informar id_procedimento, quantidade e tempo_real_minutos.';
        END IF;

        IF v_quantidade <= 0
           OR v_tempo_real <= 0 THEN
            RAISE EXCEPTION
                'Quantidade e tempo real devem ser positivos no procedimento %.',
                v_id_procedimento;
        END IF;

        IF v_inicio < p_data_hora THEN
            RAISE EXCEPTION
                'O procedimento % não pode iniciar antes do atendimento.',
                v_id_procedimento;
        END IF;

        IF NOT EXISTS (
            SELECT 1
            FROM procedimento
            WHERE id_procedimento = v_id_procedimento
        ) THEN
            RAISE EXCEPTION
                'Procedimento % não encontrado.',
                v_id_procedimento;
        END IF;

        INSERT INTO procedimento_realizado (
            id_atendimento,
            id_procedimento,
            quantidade,
            tempo_real_minutos,
            observacao,
            faturado,
            data_hora_inicio
        )
        VALUES (
            v_id_atendimento,
            v_id_procedimento,
            v_quantidade,
            v_tempo_real,
            v_item ->> 'observacao',

            COALESCE(
                (v_item ->> 'faturado')::BOOLEAN,
                FALSE
            ),

            v_inicio
        );
    END LOOP;

    RAISE NOTICE
        'Atendimento % registrado com sucesso.',
        v_id_atendimento;
END;
$$;


/* ============================================================
   2. Calcula o tempo médio de espera por unidade
   ============================================================ */

CREATE OR REPLACE PROCEDURE sp_calcular_tempo_medio_espera(
    INOUT p_resultado REFCURSOR
        DEFAULT 'resultado_tempo_espera'
)
LANGUAGE plpgsql
AS $$
BEGIN
    OPEN p_resultado FOR

        WITH primeiro_procedimento AS (
            SELECT
                id_atendimento,
                MIN(data_hora_inicio) AS primeiro_inicio

            FROM procedimento_realizado

            WHERE data_hora_inicio IS NOT NULL

            GROUP BY id_atendimento
        )

        SELECT
            u.id_unidade,
            u.nome AS unidade,

            ROUND(
                AVG(
                    EXTRACT(
                        EPOCH FROM (
                            pp.primeiro_inicio - a.data_hora
                        )
                    ) / 60
                )::NUMERIC,
                2
            ) AS media_espera_minutos,

            COUNT(*) AS atendimentos_considerados

        FROM atendimento a

        JOIN unidade u
            ON u.id_unidade = a.id_unidade

        JOIN primeiro_procedimento pp
            ON pp.id_atendimento = a.id_atendimento

        GROUP BY
            u.id_unidade,
            u.nome

        ORDER BY u.nome;
END;
$$;


/* ============================================================
   3. Reajusta as escalas de um residente
   ============================================================ */

CREATE OR REPLACE PROCEDURE sp_reajustar_escala(
    p_id_residente   BIGINT,
    p_dia_origem     VARCHAR,
    p_turno_origem   VARCHAR,
    p_dia_destino    VARCHAR,
    p_turno_destino  VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_isodow_destino  INTEGER;
    v_total_alterado  INTEGER;
BEGIN
    IF p_dia_origem NOT IN (
        'segunda',
        'terca',
        'quarta',
        'quinta',
        'sexta',
        'sabado',
        'domingo'
    )
    OR p_dia_destino NOT IN (
        'segunda',
        'terca',
        'quarta',
        'quinta',
        'sexta',
        'sabado',
        'domingo'
    ) THEN
        RAISE EXCEPTION
            'Dia da semana inválido.';
    END IF;

    IF p_turno_origem NOT IN (
        'manha',
        'tarde',
        'noite'
    )
    OR p_turno_destino NOT IN (
        'manha',
        'tarde',
        'noite'
    ) THEN
        RAISE EXCEPTION
            'Turno inválido.';
    END IF;

    v_isodow_destino := CASE p_dia_destino
        WHEN 'segunda' THEN 1
        WHEN 'terca' THEN 2
        WHEN 'quarta' THEN 3
        WHEN 'quinta' THEN 4
        WHEN 'sexta' THEN 5
        WHEN 'sabado' THEN 6
        WHEN 'domingo' THEN 7
    END;

    -- Bloqueia as escalas que serão alteradas até o fim da transação.
    PERFORM 1
    FROM escala
    WHERE id_residente = p_id_residente
      AND dia_semana = p_dia_origem
      AND turno = p_turno_origem
    FOR UPDATE;

    IF NOT FOUND THEN
        RAISE EXCEPTION
            'Nenhuma escala encontrada para o residente %, no dia % e turno %.',
            p_id_residente,
            p_dia_origem,
            p_turno_origem;
    END IF;

    -- Calcula as datas de destino e verifica possíveis conflitos.
    IF EXISTS (
        WITH destinos AS (
            SELECT
                e.id_escala,

                (
                    e.data_plantao
                    - (
                        EXTRACT(
                            ISODOW FROM e.data_plantao
                        )::INTEGER - 1
                    )
                    + (v_isodow_destino - 1)
                )::DATE AS nova_data

            FROM escala e

            WHERE e.id_residente = p_id_residente
              AND e.dia_semana = p_dia_origem
              AND e.turno = p_turno_origem
        )

        SELECT 1

        FROM destinos d

        JOIN escala existente
            ON existente.id_residente = p_id_residente
           AND existente.data_plantao = d.nova_data
           AND existente.turno = p_turno_destino
           AND existente.id_escala <> d.id_escala
    ) THEN
        RAISE EXCEPTION
            'O reajuste geraria conflito de escala para o residente %.',
            p_id_residente;
    END IF;

    UPDATE escala e
    SET
        data_plantao = (
            e.data_plantao
            - (
                EXTRACT(
                    ISODOW FROM e.data_plantao
                )::INTEGER - 1
            )
            + (v_isodow_destino - 1)
        )::DATE,

        dia_semana = p_dia_destino,
        turno = p_turno_destino

    WHERE e.id_residente = p_id_residente
      AND e.dia_semana = p_dia_origem
      AND e.turno = p_turno_origem;

    GET DIAGNOSTICS
        v_total_alterado = ROW_COUNT;

    RAISE NOTICE
        '% escala(s) reajustada(s) para % / %.',
        v_total_alterado,
        p_dia_destino,
        p_turno_destino;
END;
$$;