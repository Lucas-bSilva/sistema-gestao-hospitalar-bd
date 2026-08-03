# Relatório técnico — Etapa 2

## 1. Objetivo

A Etapa 2 amplia o Sistema de Gestão Hospitalar Dra. Yuska por meio da
implementação de funcionalidades avançadas de banco de dados e de uma camada
de aplicação desenvolvida em Python.

A evolução utiliza recursos do PostgreSQL, mapeamento objeto-relacional com
SQLAlchemy 2.x, controle transacional, concorrência e uma interface desktop
para execução e demonstração das funcionalidades.

A implementação preserva as tabelas, restrições, consultas e demais recursos
desenvolvidos na Etapa 1. Dessa forma, a nova etapa representa uma evolução
incremental do projeto, sem substituir desnecessariamente os artefatos
anteriormente avaliados.

## 2. Tecnologias e ambiente

A Etapa 2 utiliza as seguintes tecnologias:

- PostgreSQL 14 ou superior;
- Python 3.11 ou superior;
- SQLAlchemy 2.x;
- Psycopg 3;
- Python Dotenv;
- CustomTkinter;
- pgAdmin 4;
- Git e GitHub.

A variável de conexão com o banco é configurada localmente por meio do arquivo
`.env`. Esse arquivo não deve ser versionado, pois pode conter credenciais do
ambiente de desenvolvimento.

O arquivo `.env.example` apresenta somente o modelo necessário para a
configuração da conexão.

## 3. Evolução do modelo físico

A estrutura física da Etapa 1 foi ampliada com os seguintes atributos:

| Estrutura | Novo atributo | Finalidade |
|---|---|---|
| `atendimento` | `id_unidade` | identificar a unidade responsável pelo atendimento |
| `procedimento_realizado` | `data_hora_inicio` | registrar o início do procedimento e permitir o cálculo do tempo de espera |
| `procedimento` | `media_tempo_procedimento` | armazenar a média real do tempo dos procedimentos realizados |
| `escala` | `supervisao_ativa` | representar a situação da supervisão da escala |

Também foram criadas as seguintes tabelas:

- `internacao`, responsável pelo registro dos períodos de internação dos
  pacientes;
- `auditoria_atendimento`, responsável pelo histórico das operações executadas
  sobre os atendimentos.

A evolução mantém as chaves primárias e estrangeiras, restrições de domínio,
integridade referencial e regras de exclusão definidas no banco.

Também foram utilizados índices para apoiar a recuperação de informações e
impedir combinações inválidas, especialmente nas operações relacionadas às
escalas dos residentes.

A evolução estrutural está registrada principalmente nos arquivos:

- `sql/etapa2/08_evolucao_estrutura.sql`;
- `sql/etapa2/09_dados_complementares.sql`.

## 4. Procedures armazenadas

Foram implementadas três procedures para concentrar operações transacionais
que envolvem múltiplas validações e alterações no banco.

### 4.1 `sp_registrar_atendimento_completo`

Registra um atendimento e os seus respectivos procedimentos em uma única
operação.

Os procedimentos são recebidos em estrutura JSON, permitindo que vários itens
sejam processados na mesma chamada.

Caso algum paciente, profissional, unidade ou procedimento informado seja
inválido, a operação é interrompida. Como a execução é transacional, nenhuma
parte do atendimento permanece gravada quando ocorre uma falha.

### 4.2 `sp_calcular_tempo_medio_espera`

Calcula o tempo médio de espera dos pacientes por unidade.

O cálculo considera o intervalo entre o horário registrado para o atendimento
e o início do primeiro procedimento associado.

Essa procedure permite centralizar o cálculo no banco e reutilizá-lo em
consultas, relatórios e demonstrações.

### 4.3 `sp_reajustar_escala`

Realiza o reajuste da escala de um residente para uma nova data e turno.

Antes da atualização, os registros necessários são bloqueados e as regras de
conflito são verificadas. Caso o novo período já possua uma escala incompatível,
a operação é rejeitada.

As procedures estão implementadas no arquivo:

- `sql/etapa2/10_procedures.sql`.

## 5. Triggers

Foram implementadas triggers para regras que precisam ser executadas
automaticamente em resposta a operações realizadas nas tabelas.

As triggers contemplam:

- rejeição de escalas sobrepostas para o mesmo residente;
- auditoria das operações de inserção, atualização e remoção realizadas na
  tabela `atendimento`;
- recálculo automático da média real de duração dos procedimentos após
  alterações em `procedimento_realizado`.

A auditoria registra, quando aplicável:

- atendimento afetado;
- tipo de operação;
- usuário responsável;
- data e horário;
- valores anteriores;
- valores posteriores.

As triggers complementam as restrições do modelo, mas não substituem as
validações realizadas pela aplicação e pelas procedures.

A implementação está localizada no arquivo:

- `sql/etapa2/11_triggers.sql`.

## 6. Views

Foram criadas views para encapsular consultas recorrentes e facilitar a
recuperação das informações hospitalares.

As views apresentam:

- pacientes atualmente internados;
- escalas com supervisão inadequada;
- estatísticas mensais de atendimento por unidade.

A view de pacientes internados considera somente internações que ainda não
possuem data e horário de saída.

A view de supervisão permite identificar escalas com supervisão inativa ou que
não atendem aos critérios definidos para o preceptor.

A view de estatísticas mensais consolida informações dos atendimentos,
permitindo a análise dos dados por unidade e período.

As views estão implementadas no arquivo:

- `sql/etapa2/12_views.sql`.

## 7. ORM com SQLAlchemy

As tabelas do banco foram mapeadas utilizando o modelo declarativo tipado do
SQLAlchemy 2.x.

O mapeamento está concentrado principalmente em:

- `src/hospital_yuska/modelos/base.py`;
- `src/hospital_yuska/modelos/entidades.py`.

Foram representadas no ORM as entidades:

- pessoa;
- paciente;
- profissional;
- residente;
- preceptor;
- unidade;
- atendimento;
- procedimento;
- procedimento realizado;
- escala;
- internação;
- auditoria de atendimento.

Os relacionamentos entre as entidades foram configurados utilizando
`relationship`, `back_populates` e as respectivas chaves estrangeiras.

As operações originalmente desenvolvidas na Etapa 1 foram reimplementadas com
SQLAlchemy, utilizando recursos como:

- `Session`;
- `select`;
- `join`;
- `outerjoin`;
- `where`;
- `exists`;
- agregações;
- subconsultas;
- funções de janela;
- relacionamentos entre entidades.

As consultas avançadas foram implementadas por meio da linguagem de expressão
do SQLAlchemy, sem a utilização de SQL textual dentro das consultas ORM.

O projeto também demonstra duas estratégias de carregamento de
relacionamentos:

- **carregamento sob demanda**, no qual o relacionamento é consultado quando
  acessado;
- **carregamento antecipado**, no qual os relacionamentos necessários são
  carregados juntamente com a consulta principal.

## 8. Controle de concorrência

A simulação de concorrência utiliza:

- duas threads;
- duas sessões independentes do SQLAlchemy;
- duas transações concorrentes;
- bloqueio pessimista com `SELECT ... FOR UPDATE`.

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

- `scripts/simular_concorrencia.py`.

A evidência da execução é registrada em:

- `evidencias/etapa2/log_concorrencia.txt`.

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

- `src/hospital_yuska/interface/desktop.py`;
- `src/hospital_yuska/interface/servicos.py`.

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
└── __main__.py

scripts/
└── simular_concorrencia.py

evidencias/etapa2/
└── log_concorrencia.txt

docs/etapa2/
└── RELATORIO_ETAPA2.md
```

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

O arquivo 14_all_etapa2.sql centraliza a execução dos scripts SQL da Etapa 2,
respeitando a ordem necessária de criação e validação dos objetos.

## 11. Validação

A validação da Etapa 2 é realizada por meio das seguintes atividades:

- Execução da evolução estrutural;
- Inserção dos dados complementares;
- Criação das procedures;
- Criação das triggers;
- Criação das views;
- Execução de 13_testes_sql_etapa2.sql;
- Execução consolidada de 14_all_etapa2.sql;
- Teste da conexão da aplicação com o PostgreSQL;
- Compilação dos módulos Python;
- Instalação do projeto em modo editável;
- Inicialização da aplicação pelo módulo hospital_yuska;
- Execução das consultas ORM;
- Execução das consultas avançadas;
- Execução das procedures e views pela interface;
- Teste dos formulários e seletores pesquisáveis;
- Simulação de concorrência;
- Inspeção do log de concorrência em UTF-8;
- Verificação de que o arquivo .env permanece ignorado pelo Git.

## 12. Conclusão

A Etapa 2 amplia o Sistema de Gestão Hospitalar Dra. Yuska com procedures,
triggers, views, ORM, consultas avançadas, controle transacional, concorrência
e uma interface desktop integrada ao PostgreSQL.

A solução mantém a integridade e os recursos desenvolvidos na Etapa 1,
adicionando uma nova camada de aplicação sem duplicar desnecessariamente as
regras responsáveis pela consistência dos dados.

As operações críticas permanecem protegidas por transações, restrições,
triggers e mecanismos de bloqueio, enquanto a interface oferece uma forma mais
clara e eficiente de demonstrar as funcionalidades.

Dessa forma, o projeto apresenta separação entre:

- persistência e integridade no PostgreSQL;
- mapeamento e operações no SQLAlchemy;
- serviços de integração;
- apresentação por interface desktop;
- testes e evidências de execução.