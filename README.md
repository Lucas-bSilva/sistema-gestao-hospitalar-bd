# Sistema de GestÃ£o Hospitalar Dra. Yuska â€” Etapa 1

Projeto acadÃªmico desenvolvido para a disciplina de Banco de Dados com o objetivo de modelar e implementar um sistema de gestÃ£o hospitalar utilizando PostgreSQL e SQL puro.

A Etapa 1 contempla a modelagem conceitual, lÃ³gica e fÃ­sica do banco, a normalizaÃ§Ã£o atÃ© a Terceira Forma Normal, a implementaÃ§Ã£o das tabelas e restriÃ§Ãµes de integridade, a carga de dados, as operaÃ§Ãµes CRUD e as consultas analÃ­ticas solicitadas na especificaÃ§Ã£o.

> Nesta etapa nÃ£o foi utilizada ORM. A migraÃ§Ã£o para SQLAlchemy e a implementaÃ§Ã£o das funcionalidades avanÃ§adas pertencem Ã  Etapa 2.

---

## Objetivos da Etapa 1

A implementaÃ§Ã£o contempla:

- modelagem conceitual, lÃ³gica e fÃ­sica;
- elaboraÃ§Ã£o e documentaÃ§Ã£o do DER;
- normalizaÃ§Ã£o atÃ© a Terceira Forma Normal;
- criaÃ§Ã£o das tabelas e relacionamentos;
- definiÃ§Ã£o de chaves primÃ¡rias e estrangeiras;
- implementaÃ§Ã£o de restriÃ§Ãµes `CHECK`, `NOT NULL` e `UNIQUE`;
- inserÃ§Ã£o de dados para testes;
- operaÃ§Ãµes CRUD utilizando SQL puro;
- consultas bÃ¡sicas e analÃ­ticas;
- validaÃ§Ãµes automÃ¡ticas da estrutura e da carga;
- testes funcionais utilizando transaÃ§Ãµes e `ROLLBACK`.

---

## Tecnologias utilizadas

- PostgreSQL 14 ou superior;
- pgAdmin 4;
- Visual Studio Code;
- Git;
- GitHub;
- Graphviz para geraÃ§Ã£o e atualizaÃ§Ã£o do DER.

---

## Estrutura do projeto

```text
sistema-gestao-hospitalar-bd/
â”‚
â”œâ”€â”€ diagrams/
â”‚   â””â”€â”€ der.dot
â”‚
â”œâ”€â”€ docs/
â”‚   â”œâ”€â”€ DER_SGH_Dra_Yuska.pdf
â”‚   â”œâ”€â”€ MODELAGEM_E_NORMALIZACAO.md
â”‚   â””â”€â”€ ROTEIRO_APRESENTACAO.md
â”‚
â”œâ”€â”€ sql/
â”‚   â”œâ”€â”€ 01_estrutura.sql
â”‚   â”œâ”€â”€ 02_dados_teste.sql
â”‚   â”œâ”€â”€ 03_crud_consultas.sql
â”‚   â”œâ”€â”€ 04_consultas_analiticas.sql
â”‚   â”œâ”€â”€ 05_all.sql
â”‚   â”œâ”€â”€ 06_validacoes.sql
â”‚   â””â”€â”€ 07_testes_funcionais.sql
â”‚
â”œâ”€â”€ .gitignore
â””â”€â”€ README.md
```

Os scripts da pasta `sql/` sÃ£o as fontes oficiais do cÃ³digo do banco de dados.

---

## Resumo do modelo de dados

O sistema utiliza a entidade `pessoa` como base para os dados comuns de pacientes e profissionais.

```text
Pessoa
â”œâ”€â”€ Paciente
â””â”€â”€ Profissional
    â”œâ”€â”€ Residente
    â””â”€â”€ Preceptor
```

As principais relaÃ§Ãµes implementadas sÃ£o:

- um paciente pode possuir vÃ¡rios atendimentos;
- um residente pode realizar vÃ¡rios atendimentos;
- um preceptor pode supervisionar vÃ¡rios atendimentos;
- cada atendimento possui exatamente um paciente, um residente e um preceptor;
- um atendimento pode possuir vÃ¡rios procedimentos;
- um procedimento pode ser realizado em vÃ¡rios atendimentos;
- `procedimento_realizado` resolve o relacionamento muitos-para-muitos;
- uma unidade pode possuir vÃ¡rias escalas de plantÃ£o;
- cada escala relaciona unidade, data, turno, residente e preceptor.

---

## Responsabilidade dos scripts SQL

| Arquivo            | Responsabilidade |

| `01_estrutura.sql` | Recria as tabelas, chaves, relacionamentos e restriÃ§Ãµes |
| `02_dados_teste.sql` | Insere a massa inicial utilizada nas demonstraÃ§Ãµes |
| `03_crud_consultas.sql` | ContÃ©m operaÃ§Ãµes CRUD e consultas bÃ¡sicas |
| `04_consultas_analiticas.sql` | ContÃ©m as quatro consultas analÃ­ticas da especificaÃ§Ã£o |
| `05_all.sql` | Automatiza a preparaÃ§Ã£o do banco pelo cliente `psql` |
| `06_validacoes.sql` | Valida carga mÃ­nima, constraints e consistÃªncia dos dados |
| `07_testes_funcionais.sql` | Demonstra operaÃ§Ãµes com transaÃ§Ãµes finalizadas por `ROLLBACK` |

---

## Requisitos para execuÃ§Ã£o

### PostgreSQL

Ã‰ necessÃ¡rio possuir o PostgreSQL 14 ou uma versÃ£o superior.

Download:

https://www.postgresql.org/download/

Durante a instalaÃ§Ã£o:

- instalar o servidor PostgreSQL;
- instalar o pgAdmin 4;
- definir uma senha para o usuÃ¡rio `postgres`.

### pgAdmin 4

Utilizado para:

- criaÃ§Ã£o do banco;
- execuÃ§Ã£o dos scripts SQL;
- inspeÃ§Ã£o das tabelas;
- demonstraÃ§Ã£o das consultas.

### Git

Download:

https://git-scm.com/downloads

Utilizado para:

- versionamento do projeto;
- colaboraÃ§Ã£o entre os integrantes;
- registro dos commits acadÃªmicos.

### Visual Studio Code

Download:

https://code.visualstudio.com/

ExtensÃµes recomendadas:

- PostgreSQL;
- SQLTools;
- GitLens;
- Markdown Preview.

### Graphviz

NecessÃ¡rio somente para atualizar o DER a partir do arquivo `diagrams/etapa1/der.dot`.

Download:

https://graphviz.org/download/

VerificaÃ§Ã£o da instalaÃ§Ã£o:

```powershell
dot -V
```

---

## CriaÃ§Ã£o do banco

No pgAdmin:

1. conecte-se ao servidor PostgreSQL;
2. clique com o botÃ£o direito em `Databases`;
3. selecione `Create` e depois `Database`;
4. crie o banco com o nome:

```text
hospital_yuska
```

5. selecione o banco criado;
6. abra o `Query Tool`.

---

## ExecuÃ§Ã£o pelo pgAdmin

### PreparaÃ§Ã£o do banco

Execute integralmente, nesta ordem:

```text
1. sql/etapa1/01_estrutura.sql
2. sql/etapa1/02_dados_teste.sql
3. sql/etapa1/06_validacoes.sql
```

O arquivo `01_estrutura.sql` remove e recria as tabelas. Sua execuÃ§Ã£o elimina os dados existentes, portanto o arquivo `02_dados_teste.sql` deve ser executado em seguida.

### DemonstraÃ§Ã£o das funcionalidades

Depois da preparaÃ§Ã£o:

```text
4. sql/etapa1/03_crud_consultas.sql
5. sql/etapa1/04_consultas_analiticas.sql
6. sql/etapa1/07_testes_funcionais.sql
```

Os arquivos `03` e `04` devem ser executados por blocos, selecionando cada consulta atÃ© o respectivo ponto e vÃ­rgula.

O arquivo `03_crud_consultas.sql` contÃ©m comandos que alteram permanentemente os dados, como `INSERT`, `UPDATE` e `DELETE`.

Para uma demonstraÃ§Ã£o repetÃ­vel, recomenda-se utilizar o arquivo `07_testes_funcionais.sql`, pois suas alteraÃ§Ãµes sÃ£o executadas em transaÃ§Ãµes finalizadas com `ROLLBACK`.

---

## PreparaÃ§Ã£o automatizada com `psql`

O arquivo `sql/etapa1/05_all.sql` executa automaticamente:

```text
01_estrutura.sql
02_dados_teste.sql
06_validacoes.sql
```

A partir da raiz do repositÃ³rio, execute:

```powershell
psql -U postgres -d hospital_yuska -f sql/etapa1/05_all.sql
```

> O arquivo `05_all.sql` utiliza comandos `\i`, que pertencem ao cliente `psql`. Esses comandos nÃ£o devem ser executados diretamente no Query Tool do pgAdmin.

As operaÃ§Ãµes CRUD e as consultas analÃ­ticas continuam sendo demonstradas separadamente pelos arquivos `03`, `04` e `07`.

---

## Massa inicial de dados

O projeto disponibiliza uma carga superior ao mÃ­nimo exigido na especificaÃ§Ã£o:

| Entidade | Quantidade |
|---|---:|
| Pacientes | 5 |
| Residentes | 5 |
| Preceptores | 5 |
| Unidades | 4 |
| Procedimentos | 6 |
| Atendimentos | 12 |
| Procedimentos realizados | 12 |
| Escalas | 8 |

A ordem das inserÃ§Ãµes respeita as dependÃªncias entre as chaves estrangeiras:

```text
pessoa
â†’ paciente e profissional
â†’ residente e preceptor
â†’ unidade e procedimento
â†’ atendimento
â†’ procedimento_realizado
â†’ escala
```

As escalas sÃ£o criadas dentro do mÃªs corrente para garantir resultados na consulta mensal solicitada pela especificaÃ§Ã£o.

---

## RestriÃ§Ãµes de integridade

O banco utiliza:

- `PRIMARY KEY`;
- `FOREIGN KEY`;
- `NOT NULL`;
- `UNIQUE`;
- `CHECK`;
- valores padrÃ£o com `DEFAULT`;
- aÃ§Ãµes referenciais com `ON DELETE CASCADE`;
- aÃ§Ãµes referenciais com `ON DELETE RESTRICT`.

Entre as regras implementadas estÃ£o:

- CPF composto por exatamente 11 dÃ­gitos;
- CPF Ãºnico por pessoa;
- CRM Ãºnico por profissional;
- grupos sanguÃ­neos limitados aos valores vÃ¡lidos;
- ano de residÃªncia limitado a `R1`, `R2` ou `R3`;
- tipos de unidade controlados;
- capacidade de leitos nÃ£o negativa;
- duraÃ§Ã£o dos atendimentos maior que zero;
- quantidade e tempo dos procedimentos maiores que zero;
- residente e preceptor distintos no atendimento;
- turnos limitados a manhÃ£, tarde ou noite;
- coerÃªncia entre a data do plantÃ£o e o dia da semana;
- prevenÃ§Ã£o de escalas duplicadas.

---

## CRUD e consultas bÃ¡sicas

As operaÃ§Ãµes estÃ£o implementadas em:

```text
sql/etapa1/03_crud_consultas.sql
```

### InserÃ§Ã£o validada de atendimento

Antes da inserÃ§Ã£o, o script verifica a existÃªncia de:

- paciente;
- residente;
- preceptor.

A operaÃ§Ã£o utiliza CTEs e `EXISTS`. O atendimento somente Ã© inserido quando todas as referÃªncias sÃ£o vÃ¡lidas.

### Atendimentos de um paciente

Lista:

- identificador do atendimento;
- data e horÃ¡rio;
- duraÃ§Ã£o;
- paciente;
- residente;
- preceptor.

Os resultados sÃ£o ordenados cronologicamente.

### Procedimentos de um atendimento

Exibe:

- cÃ³digo;
- nome do procedimento;
- quantidade;
- tempo real;
- observaÃ§Ã£o.

### AtualizaÃ§Ã£o de paciente

Permite modificar:

- endereÃ§o;
- nÃºmero do convÃªnio.

### RemoÃ§Ã£o condicionada

Um procedimento realizado somente pode ser removido quando:

```text
faturado = FALSE
```

### MÃ©dia de duraÃ§Ã£o por residente

Calcula:

- duraÃ§Ã£o mÃ©dia dos atendimentos;
- total de atendimentos por residente.

SÃ£o utilizadas as funÃ§Ãµes:

```sql
AVG()
COUNT()
ROUND()
GROUP BY
```

---

## Consultas analÃ­ticas

As consultas estÃ£o implementadas em:

```text
sql/etapa1/04_consultas_analiticas.sql
```

### Ranking dos residentes

Classifica os residentes pelo nÃºmero de atendimentos realizados.

Utiliza:

```sql
COUNT()
DENSE_RANK()
```

### Preceptores com mais de cinco supervisÃµes

Identifica preceptores que supervisionaram mais de cinco atendimentos no perÃ­odo definido.

Utiliza:

```sql
GROUP BY
HAVING
```

### PlantÃµes por residente e unidade

Calcula a quantidade de plantÃµes no mÃªs corrente, agrupando os dados por unidade e residente.

Utiliza:

```sql
DATE_TRUNC()
CURRENT_DATE
COUNT()
GROUP BY
```

### Pacientes sem procedimento de risco alto

Lista os pacientes que nunca realizaram procedimentos classificados como `ALTO`.

Utiliza:

```sql
NOT EXISTS
```

---

## Testes funcionais

Os testes estÃ£o implementados em:

```text
sql/etapa1/07_testes_funcionais.sql
```

CaracterÃ­sticas:

- utilizaÃ§Ã£o de `BEGIN`;
- execuÃ§Ã£o de operaÃ§Ãµes de inserÃ§Ã£o, atualizaÃ§Ã£o e remoÃ§Ã£o;
- conferÃªncia dos resultados;
- finalizaÃ§Ã£o com `ROLLBACK`;
- preservaÃ§Ã£o da massa inicial;
- possibilidade de repetir os testes.

---

## ValidaÃ§Ã£o da Etapa 1

O arquivo:

```text
sql/etapa1/06_validacoes.sql
```

verifica:

- quantidade mÃ­nima de pacientes;
- quantidade mÃ­nima de residentes;
- quantidade mÃ­nima de preceptores;
- quantidade mÃ­nima de unidades;
- quantidade mÃ­nima de atendimentos;
- quantidade mÃ­nima de procedimentos realizados;
- constraints existentes no schema;
- sobreposiÃ§Ã£o indevida entre residente e preceptor;
- duplicidades de escala.

Na validaÃ§Ã£o da carga, o resultado esperado Ã©:

```text
OK
```

Nas consultas de inconsistÃªncia, o resultado esperado Ã©:

```text
0 linhas
```

---

## DocumentaÃ§Ã£o da modelagem

### DER

VersÃ£o em PDF:

```text
docs/etapa1/DER_SGH_Dra_Yuska.pdf
```

Fonte editÃ¡vel:

```text
diagrams/etapa1/der.dot
```

Para gerar novamente o PDF:

```powershell
dot -Tpdf diagrams\etapa1\der.dot -o docs\etapa1\DER_SGH_Dra_Yuska.pdf
```

### Modelo relacional e normalizaÃ§Ã£o

DisponÃ­vel em:

```text
docs/etapa1/MODELAGEM_E_NORMALIZACAO.md
```

O documento apresenta:

- justificativas das cardinalidades;
- especializaÃ§Ãµes de pessoa e profissional;
- transformaÃ§Ã£o do DER para o modelo relacional;
- anÃ¡lise das dependÃªncias funcionais;
- justificativa da normalizaÃ§Ã£o atÃ© a Terceira Forma Normal;
- decisÃµes adotadas para cumprir a especificaÃ§Ã£o.

### Roteiro de apresentaÃ§Ã£o

DisponÃ­vel em:

```text
docs/ROTEIRO_APRESENTACAO.md
```

ContÃ©m a sequÃªncia utilizada para demonstrar a modelagem, a implementaÃ§Ã£o, as validaÃ§Ãµes, o CRUD e as consultas analÃ­ticas.

---

## Campos complementares

Alguns requisitos exigiram atributos complementares ao modelo relacional inicial:

| Campo | Justificativa |
|---|---|
| `paciente.endereco` | Permitir a atualizaÃ§Ã£o do endereÃ§o |
| `procedimento.nivel_risco` | Identificar procedimentos de risco `ALTO` |
| `procedimento_realizado.faturado` | Controlar a remoÃ§Ã£o de procedimentos faturados |
| `escala.data_plantao` | Permitir consultas referentes ao mÃªs corrente |

Esses campos mantÃªm coerÃªncia com o contexto do sistema e viabilizam as operaÃ§Ãµes exigidas.

---

## RestauraÃ§Ã£o do ambiente

Para retornar o banco ao estado inicial:

```text
1. executar sql/etapa1/01_estrutura.sql;
2. executar sql/etapa1/02_dados_teste.sql;
3. executar sql/etapa1/06_validacoes.sql.
```

TambÃ©m Ã© possÃ­vel utilizar:

```powershell
psql -U postgres -d hospital_yuska -f sql/etapa1/05_all.sql
```

---

## SituaÃ§Ã£o da Etapa 1

A Etapa 1 encontra-se concluÃ­da, contemplando:

- modelagem;
- normalizaÃ§Ã£o;
- implementaÃ§Ã£o fÃ­sica;
- carga de dados;
- operaÃ§Ãµes CRUD;
- consultas bÃ¡sicas;
- consultas analÃ­ticas;
- validaÃ§Ãµes;
- testes funcionais;
- documentaÃ§Ã£o tÃ©cnica.

As funcionalidades avanÃ§adas, incluindo procedures, triggers, views, ORM e tratamento de concorrÃªncia, serÃ£o implementadas separadamente na Etapa 2.
