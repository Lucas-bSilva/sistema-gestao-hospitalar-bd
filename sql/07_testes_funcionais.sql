/*
Testes funcionais da Etapa 1.

Os testes que alteram dados usam transações finalizadas
com ROLLBACK, preservando a carga inicial do banco.
*/

-- TESTE 1: INSERÇÃO DE ATENDIMENTO COM REFERÊNCIAS VÁLIDAS

BEGIN;

WITH parametros AS (
    SELECT
        TIMESTAMP '2026-06-25 08:30' AS data_hora,
        40 AS duracao_minutos,
        1::BIGINT AS id_paciente,
        6::BIGINT AS id_residente,
        11::BIGINT AS id_preceptor
),
validacao AS (
    SELECT parametros.*
    FROM parametros
    WHERE EXISTS (
        SELECT 1
        FROM paciente
        WHERE paciente.id_pessoa = parametros.id_paciente
    )
    AND EXISTS (
        SELECT 1
        FROM residente
        WHERE residente.id_profissional = parametros.id_residente
    )
    AND EXISTS (
        SELECT 1
        FROM preceptor
        WHERE preceptor.id_profissional = parametros.id_preceptor
    )
)
INSERT INTO atendimento (
    data_hora,
    duracao_minutos,
    id_paciente,
    id_residente,
    id_preceptor
)
SELECT
    data_hora,
    duracao_minutos,
    id_paciente,
    id_residente,
    id_preceptor
FROM validacao
RETURNING *;

ROLLBACK;


-- TESTE 2: INSERÇÃO BLOQUEADA POR PACIENTE INEXISTENTE

BEGIN;

WITH parametros AS (
    SELECT
        TIMESTAMP '2026-06-25 09:30' AS data_hora,
        35 AS duracao_minutos,
        999::BIGINT AS id_paciente,
        6::BIGINT AS id_residente,
        11::BIGINT AS id_preceptor
),
validacao AS (
    SELECT parametros.*
    FROM parametros
    WHERE EXISTS (
        SELECT 1
        FROM paciente
        WHERE paciente.id_pessoa = parametros.id_paciente
    )
    AND EXISTS (
        SELECT 1
        FROM residente
        WHERE residente.id_profissional = parametros.id_residente
    )
    AND EXISTS (
        SELECT 1
        FROM preceptor
        WHERE preceptor.id_profissional = parametros.id_preceptor
    )
)
INSERT INTO atendimento (
    data_hora,
    duracao_minutos,
    id_paciente,
    id_residente,
    id_preceptor
)
SELECT
    data_hora,
    duracao_minutos,
    id_paciente,
    id_residente,
    id_preceptor
FROM validacao
RETURNING *;

ROLLBACK;


-- TESTE 3: LISTAGEM DOS ATENDIMENTOS DE UM PACIENTE

SELECT
    atendimento.id_atendimento,
    atendimento.data_hora,
    atendimento.duracao_minutos,
    paciente.nome AS paciente,
    residente.nome AS residente,
    preceptor.nome AS preceptor
FROM atendimento
JOIN pessoa paciente
    ON paciente.id_pessoa = atendimento.id_paciente
JOIN pessoa residente
    ON residente.id_pessoa = atendimento.id_residente
JOIN pessoa preceptor
    ON preceptor.id_pessoa = atendimento.id_preceptor
WHERE atendimento.id_paciente = 1
ORDER BY atendimento.data_hora;


-- TESTE 4: PROCEDIMENTOS REALIZADOS EM UM ATENDIMENTO

SELECT
    procedimento.nome AS procedimento,
    procedimento_realizado.quantidade,
    procedimento_realizado.tempo_real_minutos,
    procedimento_realizado.observacao
FROM procedimento_realizado
JOIN procedimento
    ON procedimento.id_procedimento =
       procedimento_realizado.id_procedimento
WHERE procedimento_realizado.id_atendimento = 1
ORDER BY procedimento.nome;


-- TESTE 5: ATUALIZAÇÃO CONTROLADA DE PACIENTE

BEGIN;

UPDATE paciente
SET
    endereco = 'Rua utilizada no teste, 100',
    num_convenio = 'CONV-TESTE'
WHERE id_pessoa = 1
RETURNING *;

ROLLBACK;


-- TESTE 6: REMOÇÃO DE PROCEDIMENTO NÃO FATURADO

BEGIN;

DELETE FROM procedimento_realizado
WHERE id_atendimento = 1
  AND id_procedimento = 2
  AND faturado = FALSE
RETURNING *;

ROLLBACK;


-- TESTE 7: PROCEDIMENTO FATURADO NÃO PODE SER REMOVIDO

BEGIN;

DELETE FROM procedimento_realizado
WHERE id_atendimento = 3
  AND id_procedimento = 4
  AND faturado = FALSE
RETURNING *;

ROLLBACK;


-- TESTE 8: TEMPO MÉDIO DOS ATENDIMENTOS POR RESIDENTE

SELECT
    pessoa.nome AS residente,
    ROUND(
        AVG(atendimento.duracao_minutos)::numeric,
        2
    ) AS media_duracao_minutos,
    COUNT(*) AS total_atendimentos
FROM atendimento
JOIN pessoa
    ON pessoa.id_pessoa = atendimento.id_residente
GROUP BY
    pessoa.id_pessoa,
    pessoa.nome
ORDER BY
    media_duracao_minutos DESC,
    residente;