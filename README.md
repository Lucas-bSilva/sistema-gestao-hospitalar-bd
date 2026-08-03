# Sistema de Gestão Hospitalar Dra. Yuska

Projeto acadêmico desenvolvido para a disciplina de Banco de Dados, com o objetivo de modelar, implementar e evoluir um sistema de gestão hospitalar utilizando PostgreSQL, SQL, Python e SQLAlchemy.

O desenvolvimento foi organizado em duas etapas:

- **Etapa 1 — Fundamentos:** modelagem, normalização, implementação do banco, operações CRUD e consultas analíticas com SQL puro;
- **Etapa 2 — Funcionalidades avançadas:** evolução do modelo físico, stored procedures, triggers, views, ORM, transações, concorrência e interface desktop.

> **Situação atual:** a Etapa 1 está concluída e preservada na branch `principal` e na tag `etapa1-final`. A Etapa 2 está concentrada na branch `etapa2-desenvolvimento` e encontra-se em validação final.

---

## 1. Objetivos acadêmicos

O projeto demonstra:

- modelagem conceitual, lógica e física;
- normalização até a Terceira Forma Normal;
- implementação de chaves, relacionamentos e restrições de integridade;
- operações CRUD e consultas analíticas em SQL puro;
- evolução controlada do modelo físico;
- stored procedures, triggers e views;
- mapeamento objeto-relacional com SQLAlchemy 2.x;
- uso de sessões e transações pela ORM;
- consultas utilizando a DSL do SQLAlchemy;
- comparação entre lazy loading e eager loading;
- controle de concorrência com bloqueio transacional;
- integração entre PostgreSQL, serviços Python e interface desktop;
- versionamento com Git e GitHub.

---

## 2. Tecnologias utilizadas

### Banco de dados

- PostgreSQL 14 ou superior;
- pgAdmin 4;
- SQL e PL/pgSQL.

### Aplicação

- Python 3.11 ou superior;
- SQLAlchemy 2.x;
- Psycopg 3;
- python-dotenv;
- CustomTkinter;
- Pytest.

### Desenvolvimento e documentação

- Visual Studio Code;
- Git e GitHub;
- Graphviz;
- Markdown.

As dependências oficiais estão declaradas em:

```text
pyproject.toml
requirements.txt
```

---

## 3. Escopo das etapas

### 3.1 Etapa 1 — Fundamentos

A Etapa 1 foi implementada exclusivamente com SQL puro e contempla:

- DER e modelo relacional;
- justificativa de normalização;
- criação das tabelas, chaves e restrições;
- carga de dados de teste;
- operações CRUD;
- consultas básicas e analíticas;
- validações estruturais;
- testes funcionais com transações e `ROLLBACK`.

Os scripts da Etapa 1 permanecem preservados como registro da primeira entrega.

### 3.2 Etapa 2 — Funcionalidades avançadas

A Etapa 2 evolui o projeto sem substituir os artefatos anteriores. Ela contempla:

- evolução do modelo físico;
- procedures transacionais;
- triggers de integridade, auditoria e atualização automática;
- views de acompanhamento hospitalar;
- reimplementação das operações da Etapa 1 com SQLAlchemy;
- consultas avançadas usando ORM;
- demonstração de lazy loading e eager loading;
- controle de concorrência com bloqueio pessimista;
- testes SQL e Python;
- interface desktop para demonstração das funcionalidades.

---

## 4. Estrutura principal do repositório

```text
sistema-gestao-hospitalar-bd/
|
|-- diagrams/
|   |-- der_etapa2.dot
|
|-- docs/
|   |-- etapa2/
|       |-- RELATORIO_ETAPA2.md
|
|-- evidencias/
|   |-- etapa2/
|       |-- log_concorrencia.txt
|
|-- sql/
|   |-- etapa1/
|   |   |-- 01_estrutura.sql
|   |   |-- 02_dados_teste.sql
|   |   |-- 03_crud_consultas.sql
|   |   |-- 04_consultas_analiticas.sql
|   |   |-- 05_all.sql
|   |   |-- 06_validacoes.sql
|   |   |-- 07_testes_funcionais.sql
|   |
|   |-- etapa2/
|       |-- 08_evolucao_estrutura.sql
|       |-- 09_dados_complementares.sql
|       |-- 10_procedures.sql
|       |-- 11_triggers.sql
|       |-- 12_views.sql
|       |-- 13_testes_sql_etapa2.sql
|       |-- 14_all_etapa2.sql
|
|-- scripts/
|   |-- testar_conexao.py
|   |-- simular_concorrencia.py
|
|-- src/
|   |-- hospital_yuska/
|       |-- banco.py
|       |-- config.py
|       |-- cli.py
|       |-- __main__.py
|       |-- modelos/
|       |-- repositorios/
|       |-- consultas/
|       |-- concorrencia/
|       |-- interface/
|           |-- __init__.py
|           |-- servicos.py
|           |-- desktop.py
|
|-- tests/
|-- .env.example
|-- .gitignore
|-- pyproject.toml
|-- requirements.txt
|-- README.md
```

> A estrutura acima apresenta os principais artefatos. Os scripts SQL, os módulos Python e a documentação do repositório constituem as fontes oficiais do projeto.

---

## 5. Modelo de dados

O sistema utiliza a entidade `pessoa` como base para pacientes e profissionais.

```text
Pessoa
|-- Paciente
|-- Profissional
    |-- Residente
    |-- Preceptor
```

Principais entidades:

- `pessoa`;
- `paciente`;
- `profissional`;
- `residente`;
- `preceptor`;
- `unidade`;
- `atendimento`;
- `procedimento`;
- `procedimento_realizado`;
- `escala`;
- `internacao`;
- `auditoria_atendimento`.

Principais relacionamentos:

- um paciente pode possuir vários atendimentos;
- um residente pode realizar vários atendimentos;
- um preceptor pode supervisionar vários atendimentos;
- cada atendimento está associado a paciente, residente, preceptor e unidade;
- um atendimento pode possuir vários procedimentos realizados;
- `procedimento_realizado` resolve o relacionamento muitos-para-muitos entre atendimento e procedimento;
- uma escala relaciona unidade, data, turno, residente e preceptor;
- uma internação relaciona paciente, unidade e período de permanência;
- alterações em atendimentos podem gerar registros de auditoria.

---

## 6. Integridade e regras de negócio

O banco utiliza:

- `PRIMARY KEY`;
- `FOREIGN KEY`;
- `NOT NULL`;
- `UNIQUE`;
- `CHECK`;
- `DEFAULT`;
- `ON DELETE CASCADE`;
- `ON DELETE RESTRICT`.

Entre as regras implementadas estão:

- CPF com onze dígitos e valor único;
- CRM único por profissional;
- ano de residência limitado a `R1`, `R2` ou `R3`;
- valores controlados para grupo sanguíneo, turno e dia da semana;
- duração dos atendimentos maior que zero;
- quantidade e tempo real dos procedimentos maiores que zero;
- residente e preceptor distintos em um mesmo atendimento;
- remoção de procedimento somente quando não houver faturamento associado;
- prevenção de escalas incompatíveis;
- período de internação consistente;
- auditoria de operações realizadas em atendimentos;
- atualização automática da média histórica dos procedimentos.

---

## 7. Massa de dados

A carga inicial atende e supera os quantitativos mínimos da especificação:

| Entidade | Quantidade inicial |
|---|---:|
| Pacientes | 5 |
| Residentes | 5 |
| Preceptores | 5 |
| Unidades | 4 |
| Procedimentos | 6 |
| Atendimentos | 12 |
| Procedimentos realizados | 12 |

A Etapa 2 acrescenta dados necessários para demonstrar internações, auditoria, supervisão, estatísticas mensais, médias históricas e concorrência.

---

## 8. Objetos avançados da Etapa 2

### 8.1 Stored procedures

| Procedure | Responsabilidade |
|---|---|
| `sp_registrar_atendimento_completo` | Insere atendimento e procedimentos em uma única transação |
| `sp_calcular_tempo_medio_espera` | Calcula o tempo médio de espera por unidade |
| `sp_reajustar_escala` | Reajusta escalas sem permitir conflitos |

A procedure `sp_registrar_atendimento_completo` garante atomicidade: se qualquer parte da operação falhar, toda a transação é revertida.

### 8.2 Triggers

| Trigger | Responsabilidade |
|---|---|
| `trg_check_sobreposicao_escala` | Impede sobreposição incompatível de escalas |
| `trg_audita_atendimento` | Registra inserções, atualizações e exclusões de atendimentos |
| `trg_atualiza_media_procedimentos` | Atualiza a média histórica dos procedimentos |

### 8.3 Views

| View | Responsabilidade |
|---|---|
| `vw_pacientes_internados` | Lista pacientes atualmente internados |
| `vw_residentes_sem_supervisor` | Identifica escalas com supervisão inadequada |
| `vw_estatisticas_atendimentos_mensal` | Consolida estatísticas mensais por unidade |

---

## 9. Funcionalidades implementadas com ORM

As operações da Etapa 1 foram reimplementadas com SQLAlchemy, preservando as regras de negócio e substituindo o SQL textual pela DSL da ORM.

A aplicação contempla:

- inserção validada de atendimento;
- listagem dos atendimentos de um paciente;
- listagem dos procedimentos de um atendimento;
- atualização de endereço, contato e convênio do paciente;
- remoção condicionada de procedimento realizado;
- média de duração dos atendimentos por residente;
- ranking dos residentes;
- preceptores com quantidade mínima de supervisões;
- plantões por unidade e residente;
- pacientes sem procedimentos de alto risco.

Consultas avançadas:

- preceptores que supervisionaram residentes em atendimentos de pacientes flamenguistas;
- último atendimento de cada paciente, com profissionais e procedimentos;
- percentual de procedimentos de alto risco por residente;
- comparação entre carregamento tardio e carregamento antecipado.

---

## 10. Interface desktop

A interface foi desenvolvida com CustomTkinter e organizada em quatro áreas.

### Visão geral

Permite demonstrar:

- objetos avançados do banco;
- auditoria de atendimentos;
- médias históricas dos procedimentos;
- simulação de concorrência.

### ORM — Etapa 1

Reúne as operações da primeira etapa reimplementadas com SQLAlchemy.

Os formulários utilizam:

- data e horário no padrão brasileiro `DD/MM/AAAA HH:MM`;
- seletores pesquisáveis para registros existentes;
- exibição de nomes e identificadores;
- validação dos campos antes da confirmação;
- formulários únicos para operações compostas;
- mensagens de sucesso, cancelamento ou erro.

### ORM — Avançadas

Apresenta as consultas avançadas e a comparação entre estratégias de carregamento de relacionamentos.

### Procedures e views

Permite executar e visualizar:

- pacientes internados;
- supervisão inadequada;
- estatísticas mensais;
- registro completo de atendimento;
- cálculo do tempo médio de espera;
- reajuste de escala.

A interface atua como camada de apresentação. As regras de integridade permanecem no banco de dados e nas camadas de serviço e repositório.

---

## 11. Pré-requisitos

Instale:

- PostgreSQL 14 ou superior;
- pgAdmin 4;
- Python 3.11 ou superior;
- Git;
- Graphviz, somente para regeneração do DER.

Verifique:

```powershell
python --version
pip --version
git --version
psql --version
```

---

## 12. Obtenção do projeto e acesso à Etapa 2

```powershell
git clone https://github.com/Lucas-bSilva/sistema-gestao-hospitalar-bd.git
cd sistema-gestao-hospitalar-bd
git fetch origin
git switch etapa2-desenvolvimento
git pull --rebase origin etapa2-desenvolvimento
```

Confirme:

```powershell
git branch --show-current
git status
```

Resultado esperado:

```text
etapa2-desenvolvimento
```

---

## 13. Configuração do ambiente Python

Na raiz do projeto:

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
```

O modo editável instala as dependências declaradas no `pyproject.toml` e mantém o pacote associado ao código-fonte local.

Como alternativa:

```powershell
python -m pip install -r requirements.txt
python -m pip install -e . --no-deps
```

Verifique as bibliotecas principais:

```powershell
python -c "import sqlalchemy; print('SQLAlchemy:', sqlalchemy.__version__)"
python -c "import psycopg; print('Psycopg:', psycopg.__version__)"
python -c "import customtkinter; print('CustomTkinter:', customtkinter.__version__)"
```

---

## 14. Configuração do `.env`

```powershell
Copy-Item .env.example .env
code .env
```

Exemplo:

```env
DATABASE_URL=postgresql+psycopg://hospital_app:SUA_SENHA@127.0.0.1:5432/hospital_yuska
EXIBIR_SQL=false
```

Regras:

- substitua `SUA_SENHA` pela senha local do usuário `hospital_app`;
- utilize o banco `hospital_yuska`;
- não utilize o nome incorreto `hospital_yusca`;
- não envie o arquivo `.env` ao GitHub;
- não registre senhas em scripts, logs, documentação ou commits.

Verifique se o arquivo está ignorado:

```powershell
git check-ignore -v .env
```

---

## 15. Banco e usuário da aplicação

Crie o banco:

```text
hospital_yuska
```

A aplicação utiliza preferencialmente um usuário próprio:

```sql
CREATE ROLE hospital_app
    WITH LOGIN
    PASSWORD 'SUA_SENHA_FORTE';
```

Depois de preparar as tabelas, execute como `postgres`, conectado ao banco `hospital_yuska`:

```sql
GRANT CONNECT ON DATABASE hospital_yuska TO hospital_app;
GRANT USAGE ON SCHEMA public TO hospital_app;

GRANT SELECT, INSERT, UPDATE, DELETE
ON ALL TABLES IN SCHEMA public
TO hospital_app;

GRANT USAGE, SELECT, UPDATE
ON ALL SEQUENCES IN SCHEMA public
TO hospital_app;

GRANT EXECUTE
ON ALL ROUTINES IN SCHEMA public
TO hospital_app;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO hospital_app;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO hospital_app;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT EXECUTE ON ROUTINES TO hospital_app;
```

> Caso o usuário já exista, não repita o `CREATE ROLE`. Para redefinir a senha, utilize `ALTER ROLE hospital_app PASSWORD 'NOVA_SENHA';`.

---

## 16. Execução dos scripts SQL

### Atenção

O arquivo `01_estrutura.sql` remove e recria as estruturas da Etapa 1. Sua execução elimina os dados existentes no banco selecionado.

Antes de executar qualquer script:

```sql
SELECT current_database() AS banco_atual;
```

O resultado deve ser:

```text
hospital_yuska
```

### 16.1 Etapa 1 pelo pgAdmin

Execute integralmente:

```text
1. sql/etapa1/01_estrutura.sql
2. sql/etapa1/02_dados_teste.sql
3. sql/etapa1/06_validacoes.sql
```

Para demonstrar as funcionalidades originais:

```text
4. sql/etapa1/03_crud_consultas.sql
5. sql/etapa1/04_consultas_analiticas.sql
6. sql/etapa1/07_testes_funcionais.sql
```

Os arquivos `03` e `04` devem ser executados por blocos. O arquivo `07` utiliza `ROLLBACK` para preservar a massa de dados.

### 16.2 Etapa 1 com `psql`

```powershell
psql -U postgres -d hospital_yuska -v ON_ERROR_STOP=1 -f sql/etapa1/05_all.sql
```

O arquivo `05_all.sql` utiliza comandos específicos do cliente `psql` e não deve ser executado no Query Tool do pgAdmin.

### 16.3 Etapa 2 pelo pgAdmin

Depois da Etapa 1, execute:

```text
1. sql/etapa2/08_evolucao_estrutura.sql
2. sql/etapa2/09_dados_complementares.sql
3. sql/etapa2/10_procedures.sql
4. sql/etapa2/11_triggers.sql
5. sql/etapa2/12_views.sql
6. sql/etapa2/13_testes_sql_etapa2.sql
```

### 16.4 Etapa 2 com `psql`

```powershell
psql -U postgres -d hospital_yuska -v ON_ERROR_STOP=1 -f sql/etapa2/14_all_etapa2.sql
```

> O script `14_all_etapa2.sql` deve ser executado somente depois da criação e carga da Etapa 1.

---

## 17. Teste da conexão

Com a `.venv` ativada e o `.env` configurado:

```powershell
python scripts/testar_conexao.py
```

Também é possível validar usuário e banco sem exibir a senha:

```powershell
python -c "from sqlalchemy.engine import make_url; from hospital_yuska.config import carregar_configuracao; u=make_url(carregar_configuracao().url_banco); print('Usuário:', u.username); print('Banco:', u.database)"
```

Resultado esperado:

```text
Usuário: hospital_app
Banco: hospital_yuska
```

---

## 18. Execução da aplicação

```powershell
python -m hospital_yuska
```

A aplicação deve abrir a interface desktop do Sistema de Gestão Hospitalar Dra. Yuska.

Quando o comando de console estiver instalado, também poderá ser utilizado:

```powershell
hospital-yuska
```

---

## 19. Testes

### Verificação sintática

```powershell
python -m compileall src scripts tests
```

### Testes automatizados

```powershell
python -m pytest -q
```

Testes de integração:

```powershell
python -m pytest -m integracao -q
```

Testes de concorrência:

```powershell
python -m pytest -m concorrencia -q
```

### Testes SQL

Execute:

```text
sql/etapa2/13_testes_sql_etapa2.sql
```

Os testes devem demonstrar:

- funcionamento das procedures;
- rejeição de escala conflitante;
- criação de registros de auditoria;
- atualização automática das médias;
- retorno das views.

### Simulação de concorrência

```powershell
python scripts/simular_concorrencia.py
```

Resultado esperado:

```text
Transação A obtém o bloqueio.
Transação B tenta executar a operação concorrente.
Transação A conclui o COMMIT.
Transação B é rejeitada pela regra de integridade.
Total final de escalas conflitantes: 1.
```

A evidência é salva em:

```text
evidencias/etapa2/log_concorrencia.txt
```

O arquivo é regravado a cada nova simulação. Para a entrega, mantenha uma execução final legível, em UTF-8 e sem credenciais.

---

## 20. Fluxo de demonstração pela interface

### Visão geral

1. verificar objetos do banco;
2. consultar auditoria;
3. consultar médias dos procedimentos;
4. simular concorrência.

### ORM — Etapa 1

1. inserir atendimento com os seletores;
2. listar atendimentos de um paciente;
3. consultar procedimentos de um atendimento;
4. atualizar dados do paciente;
5. testar remoção condicionada de procedimento;
6. consultar média por residente;
7. consultar ranking dos residentes;
8. consultar preceptores com quantidade mínima de atendimentos;
9. consultar plantões do mês;
10. consultar pacientes sem procedimento de alto risco.

### ORM — Avançadas

1. consultar preceptores relacionados a pacientes flamenguistas;
2. consultar o último atendimento de cada paciente;
3. consultar percentual de procedimentos de alto risco;
4. comparar carregamento tardio e antecipado.

### Procedures e views

1. consultar pacientes internados;
2. consultar supervisão inadequada;
3. consultar estatísticas mensais;
4. registrar atendimento completo;
5. calcular tempo médio de espera;
6. reajustar escala e validar conflitos.

---

## 21. Critérios de aceite

A Etapa 2 deve ser considerada validada quando:

- os scripts são executados sem erro em um banco reconstruído;
- os dados da Etapa 1 são preservados durante a evolução;
- as procedures executam conforme suas regras;
- uma falha no atendimento completo não deixa dados parciais;
- a trigger de escala rejeita sobreposições incompatíveis;
- a auditoria registra `INSERT`, `UPDATE` e `DELETE`;
- a média do procedimento é atualizada automaticamente;
- as views retornam dados coerentes;
- as operações da Etapa 1 são executadas pela ORM sem SQL textual;
- as consultas avançadas retornam resultados demonstráveis;
- lazy loading e eager loading podem ser comparados;
- a simulação concorrente mantém apenas uma escala válida;
- a interface apresenta os dados sem substituir as regras do banco;
- os testes SQL, Python e manuais são concluídos sem erros inesperados.

---

## 22. Estratégia de versionamento

```text
principal
|-- versão final da Etapa 1

tag: etapa1-final
|-- marco da primeira entrega

etapa2-desenvolvimento
|-- evolução do banco
|-- ORM e aplicação Python
|-- interface desktop
|-- testes e documentação da Etapa 2
```

Recomendações:

- desenvolver a Etapa 2 somente em `etapa2-desenvolvimento`;
- manter o Pull Request como rascunho durante os testes;
- criar commits pequenos e relacionados a uma única responsabilidade;
- não utilizar squash caso seja necessário preservar o histórico individual dos commits;
- não alterar a tag `etapa1-final`;
- revisar os arquivos modificados antes de cada `push`.

Comandos de conferência:

```powershell
git branch --show-current
git status --short
git log --oneline --decorate -10
```

---

## 23. Segurança e arquivos ignorados

Não devem ser enviados ao GitHub:

- `.env`;
- `.venv/`;
- `__pycache__/`;
- `.pytest_cache/`;
- arquivos `*.pyc`;
- arquivos `*.bak`;
- cópias como `desktop_backup.py`;
- credenciais ou URLs privadas;
- arquivos temporários do editor.

A evidência abaixo é uma exceção intencional e pode ser versionada:

```text
evidencias/etapa2/log_concorrencia.txt
```

Antes de qualquer commit:

```powershell
git status --short
git diff --check
```

---

## 24. Documentação complementar

O relatório técnico da Etapa 2 está localizado em:

```text
docs/etapa2/RELATORIO_ETAPA2.md
```

A entrega final deve preservar:

- commits separados por etapa;
- tag da versão final da Etapa 1;
- branch da Etapa 2;
- relatório técnico;
- evidência da concorrência;
- DER atualizado;
- demonstração das funcionalidades avançadas.

---

## 25. Observação final

O repositório foi organizado para permitir que cada requisito seja localizado, executado e demonstrado de forma independente.

Para uma avaliação reproduzível, recomenda-se reconstruir o banco, executar os testes SQL e Python e, somente depois, realizar a demonstração pela interface desktop.