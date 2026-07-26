/*
Testes SQL das funcionalidades avançadas.

Executar após os arquivos 08, 09, 10, 11 e 12.
Os testes que modificam dados utilizam ROLLBACK ou subtransações.
*/


/* ============================================================
   1. Conferência dos objetos criados
   ============================================================ */

SELECT
    routine_name,
    routine_type

FROM information_schema.routines

WHERE routine_schema = 'public'
  AND routine_name LIKE 'sp_%'

ORDER BY routine_name;


SELECT
    trigger_name,
    event_object_table,
    action_timing,
    event_manipulation

FROM information_schema.triggers

WHERE trigger_schema = 'public'

ORDER BY
    trigger_name,
    event_manipulation;


SELECT
    table_name

FROM information_schema.views

WHERE table_schema = 'public'
  AND table_name LIKE 'vw_%'

ORDER BY table_name;


/* ============================================================
   2. Atendimento completo válido
   ============================================================ */

BEGIN;

CALL sp_registrar_atendimento_completo(
    CURRENT_TIMESTAMP,
    45,
    1,
    6,
    11,
    1,

    '[
        {
            "id_procedimento": 1,
            "quantidade": 1,
            "tempo_real_minutos": 32,
            "observacao": "Teste da procedure",
            "faturado": false
        },
        {
            "id_procedimento": 2,
            "quantidade": 1,
            "tempo_real_minutos": 11,
            "observacao": "Segundo procedimento",
            "faturado": false
        }
    ]'::JSONB
);

SELECT *
FROM atendimento
ORDER BY id_atendimento DESC
LIMIT 1;

SELECT *
FROM procedimento_realizado
WHERE id_atendimento = (
    SELECT MAX(id_atendimento)
    FROM atendimento
)
ORDER BY id_procedimento;

ROLLBACK;


/* ============================================================
   3. Teste de atomicidade
   ============================================================ */

DO $$
DECLARE
    v_total_antes   BIGINT;
    v_total_depois  BIGINT;
BEGIN
    SELECT COUNT(*)
    INTO v_total_antes
    FROM atendimento;

    BEGIN
        CALL sp_registrar_atendimento_completo(
            CURRENT_TIMESTAMP,
            30,
            1,
            6,
            11,
            1,

            '[
                {
                    "id_procedimento": 1,
                    "quantidade": 1,
                    "tempo_real_minutos": 20
                },
                {
                    "id_procedimento": 999999,
                    "quantidade": 1,
                    "tempo_real_minutos": 15
                }
            ]'::JSONB
        );

    EXCEPTION
        WHEN OTHERS THEN
            RAISE NOTICE
                'Erro esperado capturado: %',
                SQLERRM;
    END;

    SELECT COUNT(*)
    INTO v_total_depois
    FROM atendimento;

    IF v_total_antes <> v_total_depois THEN
        RAISE EXCEPTION
            'Falha de atomicidade: o atendimento permaneceu gravado.';
    END IF;

    RAISE NOTICE
        'Atomicidade validada: nenhuma alteração parcial permaneceu.';
END;
$$;


/* ============================================================
   4. Tempo médio de espera
   ============================================================ */

BEGIN;

CALL sp_calcular_tempo_medio_espera(
    'resultado_espera'
);

FETCH ALL
FROM resultado_espera;

ROLLBACK;


/* ============================================================
   5. Auditoria de atendimento
   ============================================================ */

BEGIN;

INSERT INTO atendimento (
    data_hora,
    duracao_minutos,
    id_paciente,
    id_residente,
    id_preceptor,
    id_unidade
)
VALUES (
    CURRENT_TIMESTAMP,
    25,
    1,
    6,
    11,
    1
);

UPDATE atendimento
SET duracao_minutos = 35
WHERE id_atendimento = (
    SELECT MAX(id_atendimento)
    FROM atendimento
);

DELETE FROM atendimento
WHERE id_atendimento = (
    SELECT MAX(id_atendimento)
    FROM atendimento
);

SELECT
    operacao,
    usuario,
    dados_antigos,
    dados_novos

FROM auditoria_atendimento

ORDER BY id_auditoria DESC

LIMIT 3;

ROLLBACK;


/* ============================================================
   6. Atualização automática da média
   ============================================================ */

BEGIN;

INSERT INTO atendimento (
    data_hora,
    duracao_minutos,
    id_paciente,
    id_residente,
    id_preceptor,
    id_unidade
)
VALUES (
    CURRENT_TIMESTAMP,
    30,
    1,
    6,
    11,
    1
);

INSERT INTO procedimento_realizado (
    id_atendimento,
    id_procedimento,
    quantidade,
    tempo_real_minutos,
    observacao,
    faturado,
    data_hora_inicio
)
VALUES (
    (
        SELECT MAX(id_atendimento)
        FROM atendimento
    ),
    1,
    1,
    60,
    'Teste da média automática',
    FALSE,
    CURRENT_TIMESTAMP + INTERVAL '5 minutes'
);

SELECT
    id_procedimento,
    nome,
    media_tempo_procedimento

FROM procedimento

WHERE id_procedimento = 1;

ROLLBACK;


/* ============================================================
   7. Rejeição de sobreposição de escala
   ============================================================ */

BEGIN;

DO $$
DECLARE
    v_escala          escala%ROWTYPE;
    v_unidade_destino BIGINT;
BEGIN
    SELECT *
    INTO v_escala
    FROM escala
    ORDER BY id_escala
    LIMIT 1;

    SELECT id_unidade
    INTO v_unidade_destino
    FROM unidade
    WHERE id_unidade <> v_escala.id_unidade
    ORDER BY id_unidade
    LIMIT 1;

    BEGIN
        INSERT INTO escala (
            id_unidade,
            data_plantao,
            dia_semana,
            turno,
            id_residente,
            id_preceptor,
            supervisao_ativa
        )
        VALUES (
            v_unidade_destino,
            v_escala.data_plantao,
            v_escala.dia_semana,
            v_escala.turno,
            v_escala.id_residente,
            v_escala.id_preceptor,
            TRUE
        );

    EXCEPTION
        WHEN OTHERS THEN
            RAISE NOTICE
                'Conflito esperado capturado: %',
                SQLERRM;
    END;
END;
$$;

ROLLBACK;


/* ============================================================
   8. Reajuste de escala
   ============================================================ */

BEGIN;

-- Cria um residente temporário para isolar o teste.
INSERT INTO pessoa (
    id_pessoa,
    nome,
    cpf,
    data_nascimento,
    is_flamengo,
    telefone
)
VALUES (
    90001,
    'Residente Temporario',
    '90000000001',
    DATE '1998-01-01',
    FALSE,
    '81999990001'
);

INSERT INTO profissional (
    id_pessoa,
    crm,
    data_admissao,
    especialidade
)
VALUES (
    90001,
    'CRM-TESTE-90001',
    DATE '2029-01-01',
    'Clinica Medica'
);

INSERT INTO residente (
    id_profissional,
    ano_residencia
)
VALUES (
    90001,
    'R1'
);

INSERT INTO escala (
    id_unidade,
    data_plantao,
    dia_semana,
    turno,
    id_residente,
    id_preceptor,
    supervisao_ativa
)
VALUES (
    1,
    DATE '2030-09-02',
    'segunda',
    'manha',
    90001,
    11,
    TRUE
);

CALL sp_reajustar_escala(
    90001,
    'segunda',
    'manha',
    'terca',
    'tarde'
);

SELECT *
FROM escala
WHERE id_residente = 90001
  AND data_plantao = DATE '2030-09-03'
  AND turno = 'tarde';

ROLLBACK;


/* ============================================================
   9. Consultas das views
   ============================================================ */

SELECT *
FROM vw_pacientes_internados;

SELECT *
FROM vw_residentes_sem_supervisor;

SELECT *
FROM vw_estatisticas_atendimentos_mensal
ORDER BY
    mes,
    unidade;