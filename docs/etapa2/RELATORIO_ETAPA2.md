## 8. Controle de concorrência

A simulação de concorrência utiliza:

- duas threads;
- duas sessões independentes do SQLAlchemy;
- duas transações concorrentes;
- bloqueio pessimista com SELECT ... FOR UPDATE.

As duas transações tentam cadastrar uma escala para o mesmo residente, na
mesma data e no mesmo turno.

A primeira transação obtém o bloqueio do registro do residente, cadastra a
escala e mantém a transação ativa por alguns segundos.

A segunda transação inicia enquanto a primeira ainda possui o bloqueio e
aguarda a sua liberação.

Após o término da primeira transação, a segunda verifica novamente o estado do
banco, identifica a escala conflitante e rejeita a operação.

Ao final da demonstração, apenas uma escala conflitante deve existir no banco.

O controle combina três mecanismos:

- bloqueio pessimista na aplicação;
- trigger de validação;
- restrição de unicidade no banco.

A simulação está implementada no arquivo:

- scripts/simular_concorrencia.py.

A evidência da execução é registrada em:

- evidencias/etapa2/log_concorrencia.txt.

## 9. Interface da aplicação

A aplicação possui uma interface desktop desenvolvida com CustomTkinter.

A interface tem como objetivo facilitar a apresentação acadêmica e permitir a
execução das funcionalidades sem a necessidade de digitar comandos SQL
individualmente durante toda a demonstração.

As funcionalidades foram organizadas nas seguintes áreas:

### 9.1 Visão geral

Disponibiliza acesso a:

- verificação dos objetos da Etapa 2;
- auditoria de atendimentos;
- médias dos procedimentos;
- simulação de concorrência.

### 9.2 ORM — Etapa 1

Disponibiliza operações e consultas reimplementadas com SQLAlchemy, incluindo:

- inserção de atendimento;
- consulta dos atendimentos de um paciente;
- consulta dos procedimentos de um atendimento;
- atualização de paciente;
- remoção condicionada de procedimento;
- média de duração por residente;
- ranking de residentes;
- consulta de preceptores;
- consulta dos plantões;
- consulta de pacientes sem procedimentos de alto risco.

### 9.3 ORM — Avançadas

Disponibiliza consultas que demonstram:

- junções entre entidades;
- subconsultas;
- agregações;
- funções de janela;
- percentual de procedimentos de alto risco;
- último atendimento por paciente;
- comparação entre carregamento sob demanda e antecipado.

### 9.4 Procedures e views

Disponibiliza acesso às funcionalidades implementadas diretamente no
PostgreSQL:

- consulta de pacientes internados;
- consulta de supervisão inadequada;
- consulta de estatísticas mensais;
- registro completo de atendimento;
- cálculo do tempo médio de espera;
- reajuste de escala.

Os formulários de inserção e atualização utilizam seletores pesquisáveis para
apresentar registros existentes no banco. Essa abordagem reduz a necessidade
de o usuário memorizar identificadores numéricos e diminui o risco de
informações inválidas.

As janelas de procedimentos, atualização de paciente e cadastro de atendimento
foram organizadas de forma padronizada para facilitar a utilização e a
apresentação.

A camada gráfica está implementada principalmente em:

- src/hospital_yuska/interface/desktop.py;
- src/hospital_yuska/interface/servicos.py.

A interface não substitui as regras do banco. As validações, restrições,
procedures e triggers continuam sendo responsáveis pela integridade final dos
dados.

A aplicação também mantém uma interface de linha de comando como mecanismo
complementar de execução e diagnóstico.

## 10. Organização e rastreabilidade

Os principais artefatos da Etapa 2 estão organizados da seguinte forma:

```text
sql/etapa2/
├── 08_evolucao_estrutura.sql
├── 09_dados_complementares.sql
├── 10_procedures.sql
├── 11_triggers.sql
├── 12_views.sql
├── 13_testes_sql_etapa2.sql
└── 14_all_etapa2.sql

src/hospital_yuska/
├── consultas/
├── concorrencia/
├── interface/
├── modelos/
├── repositorios/
├── banco.py
├── cli.py
└── _main_.py

scripts/
└── simular_concorrencia.py

evidencias/etapa2/
└── log_concorrencia.txt

docs/etapa2/
└── RELATORIO_ETAPA2.md