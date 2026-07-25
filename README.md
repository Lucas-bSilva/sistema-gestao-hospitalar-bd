# Sistema de Gestão Hospitalar Dra. Yuska — Etapa 1

Projeto acadêmico desenvolvido para a disciplina de Banco de Dados com o objetivo de modelar e implementar um sistema de gestão hospitalar utilizando PostgreSQL e SQL puro.

A Etapa 1 contempla a modelagem conceitual, lógica e física do banco, a normalização até a Terceira Forma Normal, a implementação das tabelas e restrições de integridade, a carga de dados, as operações CRUD e as consultas analíticas solicitadas na especificação.

> Nesta etapa não foi utilizada ORM. A migração para SQLAlchemy e a implementação das funcionalidades avançadas pertencem à Etapa 2.

---

## Objetivos da Etapa 1

A implementação contempla:

- modelagem conceitual, lógica e física;
- elaboração e documentação do DER;
- normalização até a Terceira Forma Normal;
- criação das tabelas e relacionamentos;
- definição de chaves primárias e estrangeiras;
- implementação de restrições `CHECK`, `NOT NULL` e `UNIQUE`;
- inserção de dados para testes;
- operações CRUD utilizando SQL puro;
- consultas básicas e analíticas;
- validações automáticas da estrutura e da carga;
- testes funcionais utilizando transações e `ROLLBACK`.

---

## Tecnologias utilizadas

- PostgreSQL 14 ou superior;
- pgAdmin 4;
- Visual Studio Code;
- Git;
- GitHub;
- Graphviz para geração e atualização do DER.

---

## Estrutura do projeto

```text
sistema-gestao-hospitalar-bd/
│
├── diagrams/
│   └── der.dot
│
├── docs/
│   ├── DER_SGH_Dra_Yuska.pdf
│   ├── MODELAGEM_E_NORMALIZACAO.md
│   └── ROTEIRO_APRESENTACAO.md
│
├── sql/
│   ├── 01_estrutura.sql
│   ├── 02_dados_teste.sql
│   ├── 03_crud_consultas.sql
│   ├── 04_consultas_analiticas.sql
│   ├── 05_all.sql
│   ├── 06_validacoes.sql
│   └── 07_testes_funcionais.sql
│
├── .gitignore
└── README.md
```

Os scripts da pasta `sql/` são as fontes oficiais do código do banco de dados.

---

## Resumo do modelo de dados

O sistema utiliza a entidade `pessoa` como base para os dados comuns de pacientes e profissionais.

```text
Pessoa
├── Paciente
└── Profissional
    ├── Residente
    └── Preceptor
```

As principais relações implementadas são:

- um paciente pode possuir vários atendimentos;
- um residente pode realizar vários atendimentos;
- um preceptor pode supervisionar vários atendimentos;
- cada atendimento possui exatamente um paciente, um residente e um preceptor;
- um atendimento pode possuir vários procedimentos;
- um procedimento pode ser realizado em vários atendimentos;
- `procedimento_realizado` resolve o relacionamento muitos-para-muitos;
- uma unidade pode possuir várias escalas de plantão;
- cada escala relaciona unidade, data, turno, residente e preceptor.

---

## Responsabilidade dos scripts SQL

| Arquivo            | Responsabilidade |

| `01_estrutura.sql` | Recria as tabelas, chaves, relacionamentos e restrições |
| `02_dados_teste.sql` | Insere a massa inicial utilizada nas demonstrações |
| `03_crud_consultas.sql` | Contém operações CRUD e consultas básicas |
| `04_consultas_analiticas.sql` | Contém as quatro consultas analíticas da especificação |
| `05_all.sql` | Automatiza a preparação do banco pelo cliente `psql` |
| `06_validacoes.sql` | Valida carga mínima, constraints e consistência dos dados |
| `07_testes_funcionais.sql` | Demonstra operações com transações finalizadas por `ROLLBACK` |

---

## Requisitos para execução

### PostgreSQL

É necessário possuir o PostgreSQL 14 ou uma versão superior.

Download:

https://www.postgresql.org/download/

Durante a instalação:

- instalar o servidor PostgreSQL;
- instalar o pgAdmin 4;
- definir uma senha para o usuário `postgres`.

### pgAdmin 4

Utilizado para:

- criação do banco;
- execução dos scripts SQL;
- inspeção das tabelas;
- demonstração das consultas.

### Git

Download:

https://git-scm.com/downloads

Utilizado para:

- versionamento do projeto;
- colaboração entre os integrantes;
- registro dos commits acadêmicos.

### Visual Studio Code

Download:

https://code.visualstudio.com/

Extensões recomendadas:

- PostgreSQL;
- SQLTools;
- GitLens;
- Markdown Preview.

### Graphviz

Necessário somente para atualizar o DER a partir do arquivo `diagrams/der.dot`.

Download:

https://graphviz.org/download/

Verificação da instalação:

```powershell
dot -V
```

---

## Criação do banco

No pgAdmin:

1. conecte-se ao servidor PostgreSQL;
2. clique com o botão direito em `Databases`;
3. selecione `Create` e depois `Database`;
4. crie o banco com o nome:

```text
hospital_yuska
```

5. selecione o banco criado;
6. abra o `Query Tool`.

---

## Execução pelo pgAdmin

### Preparação do banco

Execute integralmente, nesta ordem:

```text
1. sql/01_estrutura.sql
2. sql/02_dados_teste.sql
3. sql/06_validacoes.sql
```

O arquivo `01_estrutura.sql` remove e recria as tabelas. Sua execução elimina os dados existentes, portanto o arquivo `02_dados_teste.sql` deve ser executado em seguida.

### Demonstração das funcionalidades

Depois da preparação:

```text
4. sql/03_crud_consultas.sql
5. sql/04_consultas_analiticas.sql
6. sql/07_testes_funcionais.sql
```

Os arquivos `03` e `04` devem ser executados por blocos, selecionando cada consulta até o respectivo ponto e vírgula.

O arquivo `03_crud_consultas.sql` contém comandos que alteram permanentemente os dados, como `INSERT`, `UPDATE` e `DELETE`.

Para uma demonstração repetível, recomenda-se utilizar o arquivo `07_testes_funcionais.sql`, pois suas alterações são executadas em transações finalizadas com `ROLLBACK`.

---

## Preparação automatizada com `psql`

O arquivo `sql/05_all.sql` executa automaticamente:

```text
01_estrutura.sql
02_dados_teste.sql
06_validacoes.sql
```

A partir da raiz do repositório, execute:

```powershell
psql -U postgres -d hospital_yuska -f sql/05_all.sql
```

> O arquivo `05_all.sql` utiliza comandos `\i`, que pertencem ao cliente `psql`. Esses comandos não devem ser executados diretamente no Query Tool do pgAdmin.

As operações CRUD e as consultas analíticas continuam sendo demonstradas separadamente pelos arquivos `03`, `04` e `07`.

---

## Massa inicial de dados

O projeto disponibiliza uma carga superior ao mínimo exigido na especificação:

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

A ordem das inserções respeita as dependências entre as chaves estrangeiras:

```text
pessoa
→ paciente e profissional
→ residente e preceptor
→ unidade e procedimento
→ atendimento
→ procedimento_realizado
→ escala
```

As escalas são criadas dentro do mês corrente para garantir resultados na consulta mensal solicitada pela especificação.

---

## Restrições de integridade

O banco utiliza:

- `PRIMARY KEY`;
- `FOREIGN KEY`;
- `NOT NULL`;
- `UNIQUE`;
- `CHECK`;
- valores padrão com `DEFAULT`;
- ações referenciais com `ON DELETE CASCADE`;
- ações referenciais com `ON DELETE RESTRICT`.

Entre as regras implementadas estão:

- CPF composto por exatamente 11 dígitos;
- CPF único por pessoa;
- CRM único por profissional;
- grupos sanguíneos limitados aos valores válidos;
- ano de residência limitado a `R1`, `R2` ou `R3`;
- tipos de unidade controlados;
- capacidade de leitos não negativa;
- duração dos atendimentos maior que zero;
- quantidade e tempo dos procedimentos maiores que zero;
- residente e preceptor distintos no atendimento;
- turnos limitados a manhã, tarde ou noite;
- coerência entre a data do plantão e o dia da semana;
- prevenção de escalas duplicadas.

---

## CRUD e consultas básicas

As operações estão implementadas em:

```text
sql/03_crud_consultas.sql
```

### Inserção validada de atendimento

Antes da inserção, o script verifica a existência de:

- paciente;
- residente;
- preceptor.

A operação utiliza CTEs e `EXISTS`. O atendimento somente é inserido quando todas as referências são válidas.

### Atendimentos de um paciente

Lista:

- identificador do atendimento;
- data e horário;
- duração;
- paciente;
- residente;
- preceptor.

Os resultados são ordenados cronologicamente.

### Procedimentos de um atendimento

Exibe:

- código;
- nome do procedimento;
- quantidade;
- tempo real;
- observação.

### Atualização de paciente

Permite modificar:

- endereço;
- número do convênio.

### Remoção condicionada

Um procedimento realizado somente pode ser removido quando:

```text
faturado = FALSE
```

### Média de duração por residente

Calcula:

- duração média dos atendimentos;
- total de atendimentos por residente.

São utilizadas as funções:

```sql
AVG()
COUNT()
ROUND()
GROUP BY
```

---

## Consultas analíticas

As consultas estão implementadas em:

```text
sql/04_consultas_analiticas.sql
```

### Ranking dos residentes

Classifica os residentes pelo número de atendimentos realizados.

Utiliza:

```sql
COUNT()
DENSE_RANK()
```

### Preceptores com mais de cinco supervisões

Identifica preceptores que supervisionaram mais de cinco atendimentos no período definido.

Utiliza:

```sql
GROUP BY
HAVING
```

### Plantões por residente e unidade

Calcula a quantidade de plantões no mês corrente, agrupando os dados por unidade e residente.

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

Os testes estão implementados em:

```text
sql/07_testes_funcionais.sql
```

Características:

- utilização de `BEGIN`;
- execução de operações de inserção, atualização e remoção;
- conferência dos resultados;
- finalização com `ROLLBACK`;
- preservação da massa inicial;
- possibilidade de repetir os testes.

---

## Validação da Etapa 1

O arquivo:

```text
sql/06_validacoes.sql
```

verifica:

- quantidade mínima de pacientes;
- quantidade mínima de residentes;
- quantidade mínima de preceptores;
- quantidade mínima de unidades;
- quantidade mínima de atendimentos;
- quantidade mínima de procedimentos realizados;
- constraints existentes no schema;
- sobreposição indevida entre residente e preceptor;
- duplicidades de escala.

Na validação da carga, o resultado esperado é:

```text
OK
```

Nas consultas de inconsistência, o resultado esperado é:

```text
0 linhas
```

---

## Documentação da modelagem

### DER

Versão em PDF:

```text
docs/DER_SGH_Dra_Yuska.pdf
```

Fonte editável:

```text
diagrams/der.dot
```

Para gerar novamente o PDF:

```powershell
dot -Tpdf diagrams\der.dot -o docs\DER_SGH_Dra_Yuska.pdf
```

### Modelo relacional e normalização

Disponível em:

```text
docs/MODELAGEM_E_NORMALIZACAO.md
```

O documento apresenta:

- justificativas das cardinalidades;
- especializações de pessoa e profissional;
- transformação do DER para o modelo relacional;
- análise das dependências funcionais;
- justificativa da normalização até a Terceira Forma Normal;
- decisões adotadas para cumprir a especificação.

### Roteiro de apresentação

Disponível em:

```text
docs/ROTEIRO_APRESENTACAO.md
```

Contém a sequência utilizada para demonstrar a modelagem, a implementação, as validações, o CRUD e as consultas analíticas.

---

## Campos complementares

Alguns requisitos exigiram atributos complementares ao modelo relacional inicial:

| Campo | Justificativa |
|---|---|
| `paciente.endereco` | Permitir a atualização do endereço |
| `procedimento.nivel_risco` | Identificar procedimentos de risco `ALTO` |
| `procedimento_realizado.faturado` | Controlar a remoção de procedimentos faturados |
| `escala.data_plantao` | Permitir consultas referentes ao mês corrente |

Esses campos mantêm coerência com o contexto do sistema e viabilizam as operações exigidas.

---

## Restauração do ambiente

Para retornar o banco ao estado inicial:

```text
1. executar sql/01_estrutura.sql;
2. executar sql/02_dados_teste.sql;
3. executar sql/06_validacoes.sql.
```

Também é possível utilizar:

```powershell
psql -U postgres -d hospital_yuska -f sql/05_all.sql
```

---

## Situação da Etapa 1

A Etapa 1 encontra-se concluída, contemplando:

- modelagem;
- normalização;
- implementação física;
- carga de dados;
- operações CRUD;
- consultas básicas;
- consultas analíticas;
- validações;
- testes funcionais;
- documentação técnica.

As funcionalidades avançadas, incluindo procedures, triggers, views, ORM e tratamento de concorrência, serão implementadas separadamente na Etapa 2.