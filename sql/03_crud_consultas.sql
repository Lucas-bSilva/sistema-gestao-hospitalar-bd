/*

Observacao: 
As operacoes de INSERT, UPDATE e DELETE deste arquivo alteram permanentemente
a carga do banco.

Para uma demonstracao repetivel, utilizar o arquivo
07_testes_funcionais.sql, que executa as operacoes dentro de transacoes
finalizadas com ROLLBACK.


----------------------------------------------------------------------------------------------
CRUD e consultas basicas - Etapa 1

As operacoes abaixo foram separadas por requisito para facilitar a demonstracao.
No pgAdmin, executar cada bloco completo, sempre ate o ponto e virgula (;).
*/

-- 1) Inserir novo atendimento validando paciente, residente e preceptor.
WITH parametros AS (
    SELECT
        TIMESTAMP '2026-06-20 09:00' AS data_hora,
        45 AS duracao_minutos,
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

-- Conferencia opcional do atendimento inserido.
SELECT *
FROM atendimento
ORDER BY id_atendimento DESC
LIMIT 3;

-- 2) Lista todos os atendimentos de um paciente especifico, ordenados por data.
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

-- 3) Lista os procedimentos realizados em um atendimento.
SELECT
    atendimento.id_atendimento,
    procedimento.codigo,
    procedimento.nome AS procedimento,
    procedimento_realizado.quantidade,
    procedimento_realizado.tempo_real_minutos,
    procedimento_realizado.observacao
FROM procedimento_realizado
JOIN procedimento
    ON procedimento.id_procedimento = procedimento_realizado.id_procedimento
JOIN atendimento
    ON atendimento.id_atendimento = procedimento_realizado.id_atendimento
WHERE atendimento.id_atendimento = 1
ORDER BY procedimento.nome;

-- 4) Atualiza dados de um paciente: endereco e convenio.
UPDATE paciente
SET
    endereco = 'Rua Atualizada, 123',
    num_convenio = 'CONV-001-ATUAL'
WHERE id_pessoa = 1
RETURNING *;

-- 5) Remove procedimento realizado apenas se ainda nao houver faturamento associado.
DELETE FROM procedimento_realizado
WHERE id_atendimento = 1
  AND id_procedimento = 2
  AND faturado = FALSE
RETURNING *;

-- Conferencia opcional da remocao anterior.
SELECT *
FROM procedimento_realizado
WHERE id_atendimento = 1
ORDER BY id_procedimento;

-- 6) Calcula o tempo medio de duracao dos atendimentos por residente.
SELECT
    residente.id_profissional AS id_residente,
    pessoa.nome AS residente,
    ROUND(AVG(atendimento.duracao_minutos)::numeric, 2) AS media_duracao_minutos,
    COUNT(*) AS total_atendimentos
FROM atendimento
JOIN residente
    ON residente.id_profissional = atendimento.id_residente
JOIN pessoa
    ON pessoa.id_pessoa = residente.id_profissional
GROUP BY
    residente.id_profissional,
    pessoa.nome
ORDER BY
    media_duracao_minutos DESC,
    residente;