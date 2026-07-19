# Sistema de Gestão Hospitalar Dra. Yuska — Etapa 1

Projeto acadêmico desenvolvido para a disciplina de Banco de Dados, utilizando PostgreSQL e SQL puro, sem uso de ORM, conforme os requisitos da Etapa 1 do Sistema de Gestão Hospitalar Dra. Yuska Maritan Brito.

## Objetivo da Etapa 1

Implementar:

- modelagem conceitual, lógica e física;
- normalização até a 3FN;
- criação das tabelas com restrições de integridade;
- carga inicial de dados;
- operações CRUD utilizando SQL puro;
- consultas analíticas utilizando agregações e junções;
- documentação técnica e evidências de validação.

---

# Tecnologias utilizadas

- PostgreSQL 14 ou superior
- pgAdmin 4
- Visual Studio Code
- Git
- GitHub
- Graphviz (para geração e atualização do DER)

---

# Requisitos para execução

Antes de executar os scripts, é necessário possuir instalado:

## PostgreSQL

Download:

https://www.postgresql.org/download/

Durante a instalação:

- instalar o servidor PostgreSQL;
- instalar o pgAdmin 4;
- definir uma senha para o usuário `postgres`.

---

## pgAdmin 4

Utilizado para:

- criação do banco;
- execução dos scripts SQL;
- demonstração das consultas durante a apresentação.

---

## Git

Download:

https://git-scm.com/downloads

Necessário para:

- versionamento;
- colaboração em equipe;
- controle dos commits da disciplina.

---

## Visual Studio Code

Download:

https://code.visualstudio.com/

Extensões recomendadas:

- PostgreSQL
- SQLTools
- GitLens
- Markdown Preview

---

## Graphviz

Necessário apenas para atualização do DER a partir do arquivo `.dot`.

Download:

https://graphviz.org/download/

Verificação da instalação:

```powershell
dot -V
```

---

# Estrutura do projeto

```text
sistema-gestao-hospitalar-bd/
├── diagrams/
│   └── der.dot
│
├── docs/
│   ├── DER_SGH_Dra_Yuska.pdf
│   ├── MODELAGEM_E_NORMALIZACAO.md
│   ├── ROTEIRO_APRESENTACAO.md
│   └── CODIGO_COMPLETO_POR_ARQUIVO.md
│
├── evidencias/
│   └── checklist_etapa1.md
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

---

# Criação do banco

No pgAdmin:

1. conectar ao PostgreSQL;
2. criar o banco:

```text
hospital_yuska
```

3. abrir o Query Tool desse banco.

---

# Ordem de execução recomendada

Executar os arquivos na seguinte ordem:

```text
1. sql/01_estrutura.sql
2. sql/02_dados_teste.sql
3. sql/06_validacoes.sql
4. sql/03_crud_consultas.sql
5. sql/04_consultas_analiticas.sql
6. sql/07_testes_funcionais.sql
```

---

# Preparação automatizada utilizando psql

O arquivo `sql/05_all.sql` recria a estrutura, insere a carga inicial
e executa as validações:

```powershell
psql -U postgres -d hospital_yuska -f sql/05_all.sql
```

As operações CRUD e consultas analíticas devem ser demonstradas
separadamente pelos arquivos 03, 04 e 07.


> **Observação:** o arquivo `05_all.sql` utiliza comandos `\i`,
> específicos do cliente `psql`. No Query Tool do pgAdmin,
> os scripts devem ser executados individualmente.

 1. 01_estrutura.sql
 2. 02_dados_teste.sql
 3. 06_validacoes.sql
 4. 03_crud_consultas.sql
 5. 04_consultas_analiticas.sql
 6. 07_testes_funcionais.sql

# Massa inicial de dados

O projeto disponibiliza carga mínima superior à exigida pela especificação:

| Entidade | Quantidade |
|---------|------------|
| Pacientes | 5 |
| Residentes | 5 |
| Preceptores | 5 |
| Unidades | 4 |
| Procedimentos | 6 |
| Atendimentos | 12 |
| Procedimentos realizados | 12 |

---

# Restrições implementadas

O banco utiliza:

- PRIMARY KEY;
- FOREIGN KEY;
- UNIQUE;
- CHECK;
- NOT NULL;
- integridade referencial completa entre todas as tabelas.

Exemplos:

- CPF único por pessoa;
- CRM único por profissional;
- combinação única de escala;
- valores válidos para ano da residência;
- valores válidos para turno;
- duração dos atendimentos maior que zero.

---

# Funcionalidades implementadas

## CRUD e consultas básicas

Implementadas em:

```text
sql/03_crud_consultas.sql
```

### Inserção de atendimento

Realiza validação da existência de:

- paciente;
- residente;
- preceptor.

---

### Consulta de atendimentos por paciente

Lista:

- data;
- horário;
- residente responsável;
- preceptor supervisor.

Ordenação:

```text
mais antigo → mais recente
```

---

### Consulta dos procedimentos realizados

Exibe:

- nome do procedimento;
- quantidade;
- tempo real gasto;
- observações.

---

### Atualização de dados do paciente

Permite atualização de:

- endereço;
- número do convênio.

---

### Remoção controlada de procedimentos

A remoção somente ocorre quando:

```text
faturado = FALSE
```

---

### Tempo médio dos atendimentos

Calculado por residente utilizando:

```sql
AVG()
GROUP BY
```

---

# Consultas analíticas

Implementadas em:

```text
sql/04_consultas_analiticas.sql
```

Foram implementadas:

## Ranking dos residentes

Utiliza:

```sql
DENSE_RANK()
```

---

## Preceptores com mais de cinco supervisões

Utiliza:

```sql
GROUP BY
HAVING
```

---

## Quantidade de plantões por unidade

Filtra automaticamente o mês corrente.

---

## Pacientes sem procedimentos de risco alto

Utiliza:

```sql
NOT EXISTS
```

---

# Testes funcionais

Implementados em:

```text
sql/07_testes_funcionais.sql
```

Características:

- utilização de transações;
- utilização de `ROLLBACK`;
- repetibilidade dos testes;
- preservação da carga inicial do banco.

---

# Documentação da modelagem

Disponível em:

```text
docs/MODELAGEM_E_NORMALIZACAO.md
```

Contém:

- justificativas das cardinalidades;
- justificativas das especializações;
- evidência de normalização até a 3FN;
- adequações realizadas para atender aos requisitos da etapa.

---

# Campos complementares adicionados

Alguns requisitos da especificação exigiram atributos adicionais ao modelo relacional base.

Foram adicionados:

| Campo | Motivo |
|------|--------|
| paciente.endereco | atualização de endereço do paciente |
| procedimento.nivel_risco | consulta de risco ALTO |
| procedimento_realizado.faturado | remoção condicionada |
| escala.data_plantao | filtragem do mês corrente |

---

# DER

Arquivo:

```text
docs/DER_SGH_Dra_Yuska.pdf
```

Fonte editável:

```text
diagrams/der.dot
```

Atualização do DER:

```powershell
dot -Tpdf diagrams\der.dot -o docs\DER_SGH_Dra_Yuska.pdf
```

---

# Validação da carga inicial

Arquivo:

```text
sql/06_validacoes.sql
```

Valida automaticamente:

- quantidade mínima de pacientes;
- quantidade mínima de residentes;
- quantidade mínima de preceptores;
- quantidade mínima de unidades;
- quantidade mínima de atendimentos;
- quantidade mínima de procedimentos realizados.

---

# Restauração do ambiente

Para retornar ao estado inicial do banco:

```text
1. Executar sql/01_schema.sql
2. Executar sql/02_seed.sql
3. Executar sql/06_validacoes.sql
```

---