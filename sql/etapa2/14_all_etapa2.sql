/*
Execução automatizada da estrutura completa das Etapas 1 e 2.

Executar a partir da raiz do repositório:

psql -U postgres -d hospital_yuska -f sql/etapa2/14_all_etapa2.sql
*/

\set ON_ERROR_STOP on

-- Preparação da base desenvolvida na Etapa 1.
\ir ../etapa1/01_estrutura.sql
\ir ../etapa1/02_dados_teste.sql
\ir ../etapa1/06_validacoes.sql

-- Evolução e funcionalidades avançadas da Etapa 2.
\ir 08_evolucao_estrutura.sql
\ir 09_dados_complementares.sql
\ir 10_procedures.sql
\ir 11_triggers.sql
\ir 12_views.sql