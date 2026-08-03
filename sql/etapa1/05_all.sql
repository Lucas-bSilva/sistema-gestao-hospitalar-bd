/*
Execução automatizada da Etapa 1 pelo cliente psql.

Executar a partir da raiz do repositório:

psql -U postgres -d hospital_yuska -f sql/etapa1/05_all.sql
*/

\set ON_ERROR_STOP on

\ir 01_estrutura.sql
\ir 02_dados_teste.sql
\ir 06_validacoes.sql