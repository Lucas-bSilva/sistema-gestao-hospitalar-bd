/*
Consultas analiticas - Etapa 1

Todas as consultas abaixo usam SQL puro e foram organizadas conforme os itens
solicitados na especificacao do projeto.
*/

-- 1) Ranking dos residentes por numero de atendimentos realizados.
SELECT
    DENSE_RANK() OVER (ORDER BY COUNT(atendimento.id_atendimento) DESC) AS posicao,
    pessoa.nome AS residente,
    COUNT(atendimento.id_atendimento) AS total_atendimentos
FROM residente
JOIN pessoa
    ON pessoa.id_pessoa = residente.id_profissional
LEFT JOIN atendimento
    ON atendimento.id_residente = residente.id_profissional
GROUP BY
    residente.id_profissional,
    pessoa.nome
ORDER BY
    total_atendimentos DESC,
    residente;

-- 2) Preceptores que supervisionaram mais de 5 atendimentos em determinado mes.
-- Periodo usado para teste: junho de 2026.
SELECT
    pessoa.nome AS preceptor,
    COUNT(*) AS total_supervisoes
FROM atendimento
JOIN pessoa
    ON pessoa.id_pessoa = atendimento.id_preceptor
WHERE atendimento.data_hora >= DATE '2026-06-01'
  AND atendimento.data_hora <  DATE '2026-07-01'
GROUP BY
    atendimento.id_preceptor,
    pessoa.nome
HAVING COUNT(*) > 5
ORDER BY total_supervisoes DESC;

-- 3) Para cada unidade, quantidade de plantoes escalados por residente no mes corrente.
SELECT
    unidade.nome AS unidade,
    pessoa.nome AS residente,
    COUNT(escala.id_escala) AS quantidade_plantoes_mes_corrente
FROM escala
JOIN unidade
    ON unidade.id_unidade = escala.id_unidade
JOIN pessoa
    ON pessoa.id_pessoa = escala.id_residente
WHERE escala.data_plantao >= DATE_TRUNC('month', CURRENT_DATE)
  AND escala.data_plantao <  DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '1 month'
GROUP BY
    unidade.id_unidade,
    unidade.nome,
    pessoa.nome
ORDER BY
    unidade.nome,
    quantidade_plantoes_mes_corrente DESC,
    residente;

-- 4) Pacientes que nunca realizaram procedimento de nivel de risco ALTO.
SELECT
    pessoa.id_pessoa AS id_paciente,
    pessoa.nome AS paciente,
    paciente.num_convenio
FROM paciente
JOIN pessoa
    ON pessoa.id_pessoa = paciente.id_pessoa
WHERE NOT EXISTS (
    SELECT 1
    FROM atendimento
    JOIN procedimento_realizado
        ON procedimento_realizado.id_atendimento = atendimento.id_atendimento
    JOIN procedimento
        ON procedimento.id_procedimento = procedimento_realizado.id_procedimento
    WHERE atendimento.id_paciente = paciente.id_pessoa
      AND procedimento.nivel_risco = 'ALTO'
)
ORDER BY pessoa.nome;