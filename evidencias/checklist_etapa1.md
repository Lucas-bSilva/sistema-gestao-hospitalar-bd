# Checklist de Validação - Etapa 1

## Modelagem

- [ ] DER em PDF disponível em `documentos/DER_SGH_Dra_Yuska.pdf`
- [ ] Modelo relacional documentado
- [ ] Cardinalidades explicadas
- [ ] Normalização até 3FN justificada

## Banco de Dados

- [ ] Tabelas criadas com PK
- [ ] Tabelas criadas com FK
- [ ] Campos obrigatórios com NOT NULL
- [ ] Restrições UNIQUE aplicadas
- [ ] Restrições CHECK aplicadas

## Dados mínimos

- [ ] 5 pacientes
- [ ] 5 residentes
- [ ] 5 preceptores
- [ ] 3 ou mais unidades
- [ ] 10 ou mais atendimentos
- [ ] 10 ou mais procedimentos realizados

## CRUD e consultas básicas

- [ ] Inserir atendimento validando paciente, residente e preceptor
- [ ] Listar atendimentos de paciente específico
- [ ] Listar procedimentos de um atendimento
- [ ] Atualizar convênio/endereço de paciente
- [ ] Remover procedimento apenas se não estiver faturado
- [ ] Calcular tempo médio por residente

## Consultas analíticas

- [ ] Ranking de residentes por atendimentos
- [ ] Preceptores com mais de 5 atendimentos no mês
- [ ] Plantões por unidade e residente no mês corrente
- [ ] Pacientes sem procedimento de risco ALTO