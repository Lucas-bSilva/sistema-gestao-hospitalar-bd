-- Consultas analiticas - SQL puro

-- 1) Ranking dos residentes por numero de atendimentos realizados.
SELECT
    DENSE_RANK() OVER (ORDER BY COUNT(a.id_atendimento) DESC) AS posicao,
    p.nome AS residente,
    COUNT(a.id_atendimento) AS total_atendimentos
FROM residente r
JOIN pessoa p ON p.id_pessoa = r.id_profissional
LEFT JOIN atendimento a ON a.id_residente = r.id_profissional
GROUP BY r.id_profissional, p.nome
ORDER BY total_atendimentos DESC, residente;

-- 2) Preceptores que supervisionaram mais de 5 atendimentos em um determinado mes.
-- Parametro exemplo: junho/2026.
SELECT
    p.nome AS preceptor,
    COUNT(*) AS total_supervisoes
FROM atendimento a
JOIN pessoa p ON p.id_pessoa = a.id_preceptor
WHERE a.data_hora >= DATE '2026-06-01'
  AND a.data_hora <  DATE '2026-07-01'
GROUP BY a.id_preceptor, p.nome
HAVING COUNT(*) > 5
ORDER BY total_supervisoes DESC;

-- 3) Para cada unidade, mostrar a quantidade de plantoes escalados
-- por residente no mes corrente.
SELECT
    u.nome AS unidade,
    pr.nome AS residente,
    COUNT(e.id_escala) AS quantidade_plantoes_mes_corrente
FROM unidade u
JOIN escala e ON e.id_unidade = u.id_unidade
JOIN pessoa pr ON pr.id_pessoa = e.id_residente
WHERE e.data_plantao >= DATE_TRUNC('month', CURRENT_DATE)
  AND e.data_plantao <  DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '1 month'
GROUP BY u.id_unidade, u.nome, pr.nome
ORDER BY u.nome, quantidade_plantoes_mes_corrente DESC, residente;

-- 4) Pacientes que nunca realizaram procedimento de nivel de risco ALTO.
SELECT
    p.id_pessoa AS id_paciente,
    p.nome AS paciente,
    pa.num_convenio
FROM paciente pa
JOIN pessoa p ON p.id_pessoa = pa.id_pessoa
WHERE NOT EXISTS (
    SELECT 1
    FROM atendimento a
    JOIN procedimento_realizado pr ON pr.id_atendimento = a.id_atendimento
    JOIN procedimento proc ON proc.id_procedimento = pr.id_procedimento
    WHERE a.id_paciente = pa.id_pessoa
      AND proc.nivel_risco = 'ALTO'
)
ORDER BY p.nome;
