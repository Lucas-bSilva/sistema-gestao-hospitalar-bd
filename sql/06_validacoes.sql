/*
Validações da Etapa 1.

Execute após 01_schema.sql e 02_seed.sql.
As consultas conferem carga mínima, constraints e consistência dos papéis.
*/

-- Confere a quantidade mínima de registros exigida.
SELECT 'pacientes' AS item, COUNT(*) AS total FROM paciente
UNION ALL
SELECT 'residentes', COUNT(*) FROM residente
UNION ALL
SELECT 'preceptores', COUNT(*) FROM preceptor
UNION ALL
SELECT 'unidades', COUNT(*) FROM unidade
UNION ALL
SELECT 'atendimentos', COUNT(*) FROM atendimento
UNION ALL
SELECT 'procedimentos_realizados', COUNT(*) FROM procedimento_realizado
ORDER BY item;

-- Lista as constraints criadas no schema público.
SELECT
    restricoes.table_name AS tabela,
    restricoes.constraint_name AS restricao,
    restricoes.constraint_type AS tipo
FROM information_schema.table_constraints restricoes
WHERE restricoes.table_schema = 'public'
ORDER BY
    restricoes.table_name,
    restricoes.constraint_type,
    restricoes.constraint_name;

-- O resultado esperado é zero: ninguém deve ocupar os dois papéis ao mesmo tempo.
SELECT
    pessoa.id_pessoa,
    pessoa.nome
FROM pessoa
JOIN residente
    ON residente.id_profissional = pessoa.id_pessoa
JOIN preceptor
    ON preceptor.id_profissional = pessoa.id_pessoa;

-- O resultado esperado é zero: não deve haver escala repetida pela regra do enunciado.
SELECT
    id_unidade,
    dia_semana,
    turno,
    id_residente,
    COUNT(*) AS quantidade
FROM escala
GROUP BY
    id_unidade,
    dia_semana,
    turno,
    id_residente
HAVING COUNT(*) > 1;