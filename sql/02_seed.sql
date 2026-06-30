/*
Dados de teste - Etapa 1

A carga abaixo atende aos minimos solicitados:
- 5 pacientes
- 5 residentes
- 5 preceptores
- 4 unidades
- 12 atendimentos
- 12 procedimentos realizados
*/

INSERT INTO pessoa (nome, cpf, data_nascimento, is_flamengo, telefone) VALUES
('Ana Clara Souza', '11111111111', '1995-03-10', TRUE,  '81990000001'),
('Bruno Henrique Lima', '22222222222', '1988-07-22', FALSE, '81990000002'),
('Carla Mendes Rocha', '33333333333', '2001-01-15', TRUE,  '81990000003'),
('Diego Alves Martins', '44444444444', '1979-11-30', FALSE, '81990000004'),
('Elisa Fernanda Nunes', '55555555555', '1990-05-05', TRUE,  '81990000005'),
('Felipe Araujo Costa', '66666666666', '1998-02-12', FALSE, '81990000006'),
('Gabriela Tavares Melo', '77777777777', '1997-09-18', TRUE,  '81990000007'),
('Hugo Rafael Gomes', '88888888888', '1996-12-02', FALSE, '81990000008'),
('Isabela Monteiro Reis', '99999999991', '1999-06-20', TRUE,  '81990000009'),
('Joao Pedro Almeida', '99999999992', '1998-04-08', FALSE, '81990000010'),
('Karla Bezerra Lima', '99999999993', '1975-08-14', FALSE, '81990000011'),
('Luiz Fernando Torres', '99999999994', '1970-10-11', TRUE,  '81990000012'),
('Marina Duarte Alves', '99999999995', '1980-03-27', FALSE, '81990000013'),
('Nestor Cavalcanti Rocha', '99999999996', '1968-01-09', FALSE, '81990000014'),
('Olivia Menezes Barros', '99999999997', '1982-12-19', TRUE,  '81990000015');

INSERT INTO paciente (id_pessoa, num_convenio, alergias, grupo_sanguineo, endereco) VALUES
(1, 'CONV-001', 'Dipirona', 'A+',  'Rua A, 100'),
(2, 'CONV-002', 'Nenhuma',  'O+',  'Rua B, 200'),
(3, 'CONV-003', 'Penicilina','B-',  'Rua C, 300'),
(4, 'CONV-004', 'Latex',    'AB+', 'Rua D, 400'),
(5, 'CONV-005', 'Nenhuma',  'O-',  'Rua E, 500');

INSERT INTO profissional (id_pessoa, crm, data_admissao, especialidade) VALUES
(6,  'CRM-PE-1001', '2024-02-01', 'Clinica Medica'),
(7,  'CRM-PE-1002', '2023-02-01', 'Pediatria'),
(8,  'CRM-PE-1003', '2022-02-01', 'Cirurgia Geral'),
(9,  'CRM-PE-1004', '2024-02-01', 'Urgencia'),
(10, 'CRM-PE-1005', '2023-02-01', 'Clinica Medica'),
(11, 'CRM-PE-2001', '2010-01-15', 'Clinica Medica'),
(12, 'CRM-PE-2002', '2008-03-20', 'Cirurgia Geral'),
(13, 'CRM-PE-2003', '2015-07-01', 'Pediatria'),
(14, 'CRM-PE-2004', '2005-05-10', 'UTI'),
(15, 'CRM-PE-2005', '2012-09-17', 'Urgencia');

INSERT INTO residente (id_profissional, ano_residencia) VALUES
(6, 'R1'),
(7, 'R2'),
(8, 'R3'),
(9, 'R1'),
(10, 'R2');

INSERT INTO preceptor (id_profissional, titulacao) VALUES
(11, 'doutor'),
(12, 'mestre'),
(13, 'doutor'),
(14, 'especialista'),
(15, 'doutor');

INSERT INTO unidade (nome, tipo, capacidade_leitos) VALUES
('Enfermaria Geral', 'Enfermaria', 40),
('UTI Adulto', 'UTI', 12),
('Pronto-Socorro Central', 'Pronto-Socorro', 20),
('Ambulatorio Escola', 'Ambulatorio', 10);

INSERT INTO procedimento (codigo, nome, tempo_medio_minutos, nivel_risco) VALUES
('PROC-001', 'Sutura simples', 30, 'MEDIO'),
('PROC-002', 'Coleta de sangue', 10, 'BAIXO'),
('PROC-003', 'Aplicacao de medicacao', 15, 'BAIXO'),
('PROC-004', 'Drenagem de abscesso', 45, 'ALTO'),
('PROC-005', 'Curativo especial', 25, 'MEDIO'),
('PROC-006', 'Intubacao orotraqueal', 20, 'ALTO');

INSERT INTO atendimento (data_hora, duracao_minutos, id_paciente, id_residente, id_preceptor) VALUES
('2026-06-01 08:30', 50, 1, 6, 11),
('2026-06-02 09:00', 35, 2, 7, 12),
('2026-06-03 14:20', 70, 3, 8, 11),
('2026-06-04 19:10', 45, 4, 9, 13),
('2026-06-05 10:15', 40, 5, 10, 14),
('2026-06-06 11:30', 55, 1, 6, 11),
('2026-06-07 15:45', 60, 2, 7, 11),
('2026-06-08 20:00', 80, 3, 8, 15),
('2026-06-09 08:00', 25, 4, 9, 13),
('2026-06-10 13:00', 65, 5, 10, 11),
('2026-06-11 09:30', 30, 1, 7, 11),
('2026-06-12 10:00', 32, 2, 6, 11);

INSERT INTO procedimento_realizado (id_atendimento, id_procedimento, quantidade, tempo_real_minutos, observacao, faturado) VALUES
(1, 1, 1, 35, 'Sutura sem intercorrencias', FALSE),
(1, 2, 1, 12, 'Coleta inicial', FALSE),
(2, 3, 1, 16, 'Medicacao administrada', FALSE),
(3, 4, 1, 50, 'Drenagem com dor local', TRUE),
(4, 5, 2, 30, 'Curativos trocados', FALSE),
(5, 2, 1, 9,  'Coleta rapida', FALSE),
(6, 3, 2, 28, 'Duas aplicacoes', FALSE),
(7, 6, 1, 22, 'Procedimento critico estabilizado', TRUE),
(8, 4, 1, 47, 'Drenagem com sangramento leve', FALSE),
(9, 2, 1, 10, 'Coleta sem intercorrencias', FALSE),
(10, 5, 1, 25, 'Curativo planejado', FALSE),
(11, 3, 1, 14, 'Medicacao sem reacao', FALSE);

INSERT INTO escala (id_unidade, data_plantao, dia_semana, turno, id_residente, id_preceptor) VALUES
(1, DATE_TRUNC('month', CURRENT_DATE)::date + 1, 'segunda', 'manha', 6, 11),
(2, DATE_TRUNC('month', CURRENT_DATE)::date + 2, 'segunda', 'tarde', 7, 12),
(3, DATE_TRUNC('month', CURRENT_DATE)::date + 3, 'terca', 'noite', 8, 13),
(4, DATE_TRUNC('month', CURRENT_DATE)::date + 4, 'quarta', 'manha', 9, 14),
(1, DATE_TRUNC('month', CURRENT_DATE)::date + 5, 'quinta', 'tarde', 10, 15),
(2, DATE_TRUNC('month', CURRENT_DATE)::date + 6, 'sexta', 'noite', 6, 11),
(3, DATE_TRUNC('month', CURRENT_DATE)::date + 7, 'sabado', 'manha', 7, 13),
(4, DATE_TRUNC('month', CURRENT_DATE)::date + 8, 'domingo', 'tarde', 8, 15);