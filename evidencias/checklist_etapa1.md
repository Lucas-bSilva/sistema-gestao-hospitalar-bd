
### Arquivo 2 — `evidencias/checklist_etapa1.md`


# Checklist de validação — Etapa 1

## Modelagem

- [ ] DER disponível em `docs/DER_SGH_Dra_Yuska.pdf`
- [ ] DER compatível com `sql/01_schema.sql`
- [ ] Cardinalidades justificadas
- [ ] Especializações justificadas
- [ ] Normalização até a 3FN explicada

## Estrutura do banco

- [ ] Todas as tabelas foram criadas
- [ ] Chaves primárias conferidas
- [ ] Chaves estrangeiras conferidas
- [ ] Restrições `NOT NULL` conferidas
- [ ] Restrições `UNIQUE` conferidas
- [ ] Restrições `CHECK` conferidas

## Dados mínimos

- [ ] 5 pacientes
- [ ] 5 residentes
- [ ] 5 preceptores
- [ ] 3 ou mais unidades
- [ ] 10 ou mais atendimentos
- [ ] 10 ou mais procedimentos realizados

## CRUD e consultas básicas

- [ ] Inserção com validação das referências
- [ ] Listagem de atendimentos por paciente
- [ ] Listagem de procedimentos por atendimento
- [ ] Atualização de endereço ou convênio
- [ ] Exclusão condicionada ao faturamento
- [ ] Média da duração por residente

## Consultas analíticas

- [ ] Ranking dos residentes
- [ ] Preceptores com mais de cinco supervisões
- [ ] Plantões por unidade e residente no mês
- [ ] Pacientes sem procedimento de risco alto

## Apresentação

- [ ] Banco restaurado antes da demonstração
- [ ] Scripts abertos previamente
- [ ] Consultas executadas individualmente
- [ ] Resultados esperados conferidos
- [ ] Apresentação concluída em até 15 minutos