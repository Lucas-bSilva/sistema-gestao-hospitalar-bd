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
