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