/*
Views da Etapa 2.
*/


/* ============================================================
   1. Pacientes atualmente internados
   ============================================================ */

CREATE OR REPLACE VIEW vw_pacientes_internados AS

WITH internacao_mais_recente AS (
    SELECT
        i.*,

        ROW_NUMBER() OVER (
            PARTITION BY i.id_paciente
            ORDER BY
                i.data_hora_entrada DESC,
                i.id_internacao DESC
        ) AS ordem

    FROM internacao i
)

SELECT
    i.id_internacao,
    p.id_pessoa AS id_paciente,
    pe.nome AS paciente,
    u.id_unidade,
    u.nome AS unidade,
    i.data_hora_entrada

FROM internacao_mais_recente i

JOIN paciente p
    ON p.id_pessoa = i.id_paciente

JOIN pessoa pe
    ON pe.id_pessoa = p.id_pessoa

JOIN unidade u
    ON u.id_unidade = i.id_unidade

WHERE i.ordem = 1
  AND i.data_hora_saida IS NULL;


/* ============================================================
   2. Residentes sem supervisão adequada
   ============================================================ */

CREATE OR REPLACE VIEW vw_residentes_sem_supervisor AS

SELECT
    e.id_escala,
    e.data_plantao,
    e.dia_semana,
    e.turno,

    u.id_unidade,
    u.nome AS unidade,

    r.id_profissional AS id_residente,
    pessoa_residente.nome AS residente,

    pr.id_profissional AS id_preceptor,
    pessoa_preceptor.nome AS preceptor,

    pr.titulacao,
    e.supervisao_ativa

FROM escala e

JOIN unidade u
    ON u.id_unidade = e.id_unidade

JOIN residente r
    ON r.id_profissional = e.id_residente

JOIN pessoa pessoa_residente
    ON pessoa_residente.id_pessoa =
       r.id_profissional

JOIN preceptor pr
    ON pr.id_profissional = e.id_preceptor

JOIN pessoa pessoa_preceptor
    ON pessoa_preceptor.id_pessoa =
       pr.id_profissional

WHERE e.supervisao_ativa = FALSE
   OR LOWER(TRIM(pr.titulacao)) <> 'doutor';


/* ============================================================
   3. Estatísticas mensais por unidade
   ============================================================ */

CREATE OR REPLACE VIEW
    vw_estatisticas_atendimentos_mensal AS

WITH resumo_atendimentos AS (
    SELECT
        DATE_TRUNC(
            'month',
            a.data_hora
        )::DATE AS mes,

        a.id_unidade,

        COUNT(*) AS total_atendimentos,

        ROUND(
            AVG(a.duracao_minutos)::NUMERIC,
            2
        ) AS media_duracao_minutos

    FROM atendimento a

    GROUP BY
        DATE_TRUNC(
            'month',
            a.data_hora
        )::DATE,

        a.id_unidade
),

frequencia_procedimentos AS (
    SELECT
        DATE_TRUNC(
            'month',
            a.data_hora
        )::DATE AS mes,

        a.id_unidade,
        p.nome AS procedimento,

        SUM(pr.quantidade) AS total_execucoes

    FROM atendimento a

    JOIN procedimento_realizado pr
        ON pr.id_atendimento =
           a.id_atendimento

    JOIN procedimento p
        ON p.id_procedimento =
           pr.id_procedimento

    GROUP BY
        DATE_TRUNC(
            'month',
            a.data_hora
        )::DATE,

        a.id_unidade,
        p.nome
),

procedimentos_classificados AS (
    SELECT
        fp.*,

        DENSE_RANK() OVER (
            PARTITION BY
                fp.mes,
                fp.id_unidade

            ORDER BY
                fp.total_execucoes DESC
        ) AS posicao

    FROM frequencia_procedimentos fp
),

procedimentos_mais_comuns AS (
    SELECT
        mes,
        id_unidade,

        STRING_AGG(
            procedimento,
            ', '
            ORDER BY procedimento
        ) AS procedimentos_mais_comuns

    FROM procedimentos_classificados

    WHERE posicao = 1

    GROUP BY
        mes,
        id_unidade
)

SELECT
    ra.mes,

    u.id_unidade,
    u.nome AS unidade,

    ra.total_atendimentos,
    ra.media_duracao_minutos,

    COALESCE(
        pmc.procedimentos_mais_comuns,
        'Nenhum procedimento'
    ) AS procedimentos_mais_comuns

FROM resumo_atendimentos ra

JOIN unidade u
    ON u.id_unidade = ra.id_unidade

LEFT JOIN procedimentos_mais_comuns pmc
    ON pmc.mes = ra.mes
   AND pmc.id_unidade = ra.id_unidade;


DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM pg_roles
        WHERE rolname = 'hospital_app'
    ) THEN
        GRANT SELECT ON
            vw_pacientes_internados,
            vw_residentes_sem_supervisor,
            vw_estatisticas_atendimentos_mensal
        TO hospital_app;
    END IF;
END;
$$;