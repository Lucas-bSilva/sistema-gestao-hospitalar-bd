# Relatório técnico — Etapa 2

## 1. Objetivo

A Etapa 2 amplia o Sistema de Gestão Hospitalar Dra. Yuska com recursos
avançados de PostgreSQL e uma camada de aplicação desenvolvida em Python
com SQLAlchemy 2.x.

A evolução preserva as tabelas e funcionalidades implementadas na Etapa 1,
evitando a substituição desnecessária dos scripts anteriormente avaliados.

## 2. Evolução do modelo físico

Foram acrescentados os seguintes atributos:

| Estrutura | Novo atributo | Finalidade |
|---|---|---|
| atendimento | id_unidade | identificar a unidade responsável |
| procedimento_realizado | data_hora_inicio | calcular o tempo de espera |
| procedimento | media_tempo_procedimento | armazenar a média real |
| escala | supervisao_ativa | representar a supervisão vigente |

Também foram criadas:

- `internacao`, responsável pelos períodos de internação;
- `auditoria_atendimento`, responsável pelo histórico de alterações.

O modelo utiliza chaves, restrições, índices e integridade referencial para
evitar dados inválidos e melhorar a recuperação das informações.

## 3. Stored procedures

Foram implementadas três procedures:

### sp_registrar_atendimento_completo

Registra o atendimento e todos os procedimentos recebidos em um array JSON.
Caso qualquer procedimento seja inválido, toda a operação é desfeita.

### sp_calcular_tempo_medio_espera

Calcula, por unidade, o intervalo médio entre a chegada do paciente e o início
do primeiro procedimento.

### sp_reajustar_escala

Move as escalas de um residente para outro dia e turno. Antes da alteração,
bloqueia os registros e verifica possíveis conflitos.

## 4. Triggers

Foram implementadas três regras automáticas:

- rejeição de escalas sobrepostas;
- auditoria de INSERT, UPDATE e DELETE em atendimento;
- recálculo da média real do procedimento após nova realização.

As triggers foram usadas apenas em situações que precisam ser executadas
automaticamente em resposta a eventos das tabelas.

## 5. Views

As views implementadas apresentam:

- pacientes atualmente internados;
- residentes com supervisão inativa ou preceptor sem titulação de doutor;
- estatísticas mensais de atendimento por unidade.

As views encapsulam consultas recorrentes e facilitam a apresentação dos
resultados.

## 6. ORM com SQLAlchemy

Todas as tabelas foram mapeadas utilizando o modelo declarativo do
SQLAlchemy 2.x.

As operações da Etapa 1 foram reimplementadas com:

- `Session`;
- `select`;
- `join` e `outerjoin`;
- `where`;
- `exists`;
- agregações;
- funções de janela;
- relacionamentos entre entidades.

As consultas avançadas foram implementadas sem SQL textual.

O projeto demonstra:

- lazy loading, no qual o relacionamento é carregado sob demanda;
- eager loading, no qual os relacionamentos são carregados antecipadamente.

## 7. Concorrência

A simulação utiliza duas threads e duas sessões independentes.

As duas transações tentam cadastrar uma escala para o mesmo residente, data
e turno. A primeira transação bloqueia a linha do residente utilizando
`SELECT ... FOR UPDATE`.

A segunda transação aguarda o término da primeira e, após a liberação,
identifica a escala conflitante e rejeita a operação.

O controle combina:

- bloqueio pessimista;
- trigger de validação;
- índice único no banco.

## 8. Interface

Foi adotada uma interface de linha de comando porque ela permite demonstrar
as funcionalidades da Etapa 2 com menor complexidade e sem introduzir um
framework web que não é exigido pela especificação.

A CLI oferece acesso às consultas, views, estratégias de carregamento e
relatórios principais.

## 9. Validação

A validação é realizada por meio de:

- `13_testes_sql_etapa2.sql`;
- teste de conexão Python;
- compilação dos módulos;
- execução da CLI;
- simulação de concorrência;
- inspeção do log gerado.

## 10. Conclusão

A Etapa 2 adiciona procedures, triggers, views, ORM, consultas avançadas,
transações e concorrência sem comprometer a estrutura aprovada na Etapa 1.