/*
Validacoes rapidas - Etapa 1

Use este script depois de executar 01_schema.sql e 02_seed.sql.
Ele ajuda a conferir se os dados minimos e as principais restricoes foram criados.
*/

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
SELECT 'procedimentos_realizados', COUNT(*) FROM procedimento_realizado;

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