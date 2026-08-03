/*
Dados complementares da Etapa 2.

O script preenche os atributos acrescentados à estrutura, cria exemplos
necessários para as views e torna obrigatórios os novos campos depois que
os registros existentes forem atualizados.
*/

BEGIN;

-- Distribui os atendimentos existentes entre as quatro unidades.
UPDATE atendimento
SET id_unidade = CASE
    WHEN id_atendimento IN (1, 6, 11) THEN 1
    WHEN id_atendimento IN (2, 7, 12) THEN 4
    WHEN id_atendimento IN (3, 8) THEN 2
    ELSE 3
END
WHERE id_unidade IS NULL;

-- Calcula horários de início coerentes para os procedimentos existentes.
WITH procedimentos_ordenados AS (
    SELECT
        pr.id_atendimento,
        pr.id_procedimento,

        a.data_hora
            + MAKE_INTERVAL(
                mins => (
                    10
                    + 15 * (
                        ROW_NUMBER() OVER (
                            PARTITION BY pr.id_atendimento
                            ORDER BY pr.id_procedimento
                        ) - 1
                    )
                )::INTEGER
            ) AS inicio_calculado

    FROM procedimento_realizado pr

    JOIN atendimento a
        ON a.id_atendimento = pr.id_atendimento
)
UPDATE procedimento_realizado pr
SET data_hora_inicio = po.inicio_calculado
FROM procedimentos_ordenados po
WHERE po.id_atendimento = pr.id_atendimento
  AND po.id_procedimento = pr.id_procedimento
  AND pr.data_hora_inicio IS NULL;

-- Inicializa a média histórica antes da instalação da trigger.
UPDATE procedimento p
SET media_tempo_procedimento = medias.media_minutos
FROM (
    SELECT
        id_procedimento,
        ROUND(
            AVG(tempo_real_minutos)::NUMERIC,
            2
        ) AS media_minutos

    FROM procedimento_realizado

    GROUP BY id_procedimento
) medias
WHERE medias.id_procedimento = p.id_procedimento;

-- Internação ativa para a view de pacientes internados.
INSERT INTO internacao (
    id_paciente,
    id_unidade,
    data_hora_entrada,
    data_hora_saida
)
SELECT
    1,
    1,
    CURRENT_TIMESTAMP - INTERVAL '2 days',
    NULL
WHERE NOT EXISTS (
    SELECT 1
    FROM internacao
    WHERE id_paciente = 1
      AND data_hora_saida IS NULL
);

-- Internação encerrada para diferenciar registros ativos e concluídos.
INSERT INTO internacao (
    id_paciente,
    id_unidade,
    data_hora_entrada,
    data_hora_saida
)
SELECT
    3,
    2,
    CURRENT_TIMESTAMP - INTERVAL '8 days',
    CURRENT_TIMESTAMP - INTERVAL '5 days'
WHERE NOT EXISTS (
    SELECT 1
    FROM internacao
    WHERE id_paciente = 3
      AND data_hora_entrada::DATE =
          (CURRENT_TIMESTAMP - INTERVAL '8 days')::DATE
);

-- Cria uma situação de supervisão inativa para demonstração da view.
UPDATE escala
SET supervisao_ativa = FALSE
WHERE id_escala = (
    SELECT MIN(e.id_escala)

    FROM escala e

    JOIN preceptor pr
        ON pr.id_profissional = e.id_preceptor

    WHERE LOWER(TRIM(pr.titulacao)) = 'doutor'
);

-- Depois do preenchimento, os novos campos passam a ser obrigatórios.
ALTER TABLE atendimento
    ALTER COLUMN id_unidade SET NOT NULL;

ALTER TABLE procedimento_realizado
    ALTER COLUMN data_hora_inicio SET NOT NULL;

COMMIT;

-- ============================================================
-- DADOS COMPLEMENTARES PARA DEMONSTRAÇÃO DA ETAPA 2
-- ============================================================

BEGIN;

-- ------------------------------------------------------------
-- 1. Padronização do convênio da paciente Ana Clara
-- ------------------------------------------------------------
-- O valor foi restaurado para o padrão utilizado na carga inicial.
UPDATE paciente
SET num_convenio = 'CONV-001'
WHERE id_pessoa = 1
  AND COALESCE(num_convenio, '') <> 'CONV-001';


-- ------------------------------------------------------------
-- 2. Atendimentos de agosto de 2026
-- ------------------------------------------------------------
-- Os registros garantem que o preceptor 11 possua pelo menos
-- seis atendimentos no mesmo mês, permitindo demonstrar a
-- consulta "Preceptores com mais de cinco atendimentos".
WITH novos_atendimentos (
    data_hora,
    duracao_minutos,
    id_paciente,
    id_residente,
    id_preceptor,
    id_unidade
) AS (
    VALUES
        (
            TIMESTAMP '2026-08-01 08:00:00',
            40,
            1,
            6,
            11,
            1
        ),
        (
            TIMESTAMP '2026-08-01 09:30:00',
            35,
            2,
            7,
            11,
            2
        ),
        (
            TIMESTAMP '2026-08-01 11:00:00',
            50,
            3,
            8,
            11,
            3
        ),
        (
            TIMESTAMP '2026-08-01 14:00:00',
            45,
            4,
            9,
            11,
            4
        ),
        (
            TIMESTAMP '2026-08-01 16:00:00',
            30,
            5,
            10,
            11,
            1
        ),
        (
            TIMESTAMP '2026-08-02 08:00:00',
            55,
            2,
            6,
            11,
            2
        )
)
INSERT INTO atendimento (
    data_hora,
    duracao_minutos,
    id_paciente,
    id_residente,
    id_preceptor,
    id_unidade
)
SELECT
    novo.data_hora,
    novo.duracao_minutos,
    novo.id_paciente,
    novo.id_residente,
    novo.id_preceptor,
    novo.id_unidade
FROM novos_atendimentos AS novo
WHERE NOT EXISTS (
    SELECT 1
    FROM atendimento AS existente
    WHERE existente.data_hora = novo.data_hora
      AND existente.id_paciente = novo.id_paciente
      AND existente.id_residente = novo.id_residente
      AND existente.id_preceptor = novo.id_preceptor
      AND existente.id_unidade = novo.id_unidade
);


-- ------------------------------------------------------------
-- 3. Plantões de agosto de 2026
-- ------------------------------------------------------------
-- Os plantões são distribuídos entre residentes, preceptores,
-- unidades, datas e turnos diferentes, evitando sobreposição.
WITH novas_escalas (
    data_plantao,
    dia_semana,
    turno,
    id_unidade,
    id_residente,
    id_preceptor,
    supervisao_ativa
) AS (
    VALUES
        (
            DATE '2026-08-10',
            'segunda',
            'manha',
            1,
            6,
            11,
            TRUE
        ),
        (
            DATE '2026-08-11',
            'terca',
            'tarde',
            2,
            7,
            12,
            TRUE
        ),
        (
            DATE '2026-08-12',
            'quarta',
            'noite',
            3,
            8,
            13,
            TRUE
        ),
        (
            DATE '2026-08-14',
            'sexta',
            'manha',
            4,
            9,
            14,
            TRUE
        )
)
INSERT INTO escala (
    data_plantao,
    dia_semana,
    turno,
    id_unidade,
    id_residente,
    id_preceptor,
    supervisao_ativa
)
SELECT
    nova.data_plantao,
    nova.dia_semana,
    nova.turno,
    nova.id_unidade,
    nova.id_residente,
    nova.id_preceptor,
    nova.supervisao_ativa
FROM novas_escalas AS nova
WHERE NOT EXISTS (
    SELECT 1
    FROM escala AS existente
    WHERE existente.id_residente = nova.id_residente
      AND existente.data_plantao = nova.data_plantao
      AND existente.turno = nova.turno
);

COMMIT;