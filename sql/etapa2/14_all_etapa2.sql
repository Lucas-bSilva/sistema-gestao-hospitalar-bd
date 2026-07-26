/*
Execução completa pelo cliente psql.
Executar a partir da raiz do repositório:

psql -U postgres -d hospital_yuska -f sql/etapa2/14_all_etapa2.sql
*/

\set ON_ERROR_STOP on

\ir ../01_estrutura.sql
\ir ../02_dados_teste.sql
\ir ../06_validacoes.sql
\ir 08_evolucao_estrutura.sql
\ir 09_dados_complementares.sql
\ir 10_procedures.sql
\ir 11_triggers.sql
\ir 12_views.sql
\ir 13_testes_sql_etapa2.sql