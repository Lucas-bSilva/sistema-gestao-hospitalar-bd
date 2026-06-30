-- Validacoes rapidas da Etapa 1.
-- Este arquivo serve para conferir se a carga minima exigida foi inserida corretamente.

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

-- Conferencia das principais restricoes cadastradas no schema public.
SELECT
    tc.table_name,
    tc.constraint_name,
    tc.constraint_type
FROM information_schema.table_constraints tc
WHERE tc.table_schema = 'public'
ORDER BY tc.table_name, tc.constraint_type, tc.constraint_name;