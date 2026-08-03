# Modelagem e Normalizacao - Etapa 1

A implementaÃ§Ã£o consegue detectar profissionais cadastrados simultaneamente
como residente e preceptor por meio de uma consulta de validaÃ§Ã£o presente em
`sql/etapa1/06_validacoes.sql`.

Entretanto, com a estrutura de especializaÃ§Ã£o baseada exclusivamente em
tabelas separadas, uma constraint CHECK nÃ£o consegue consultar a outra tabela.
Assim, a exclusividade entre os papÃ©is nÃ£o Ã© garantida de forma preventiva
nesta etapa.

A garantia automÃ¡tica poderÃ¡ ser implementada posteriormente por uma trigger,
por um atributo discriminador de papel vigente ou por uma tabela histÃ³rica
com perÃ­odos de vigÃªncia. Para a Etapa 1, a equipe preservou o modelo
relacional fornecido no enunciado e documentou essa limitaÃ§Ã£o.

## 1. Entidades principais

O projeto representa o Hospital Universitario Dra. Yuska Maritan Brito com as entidades Pessoa, Paciente, Profissional, Residente, Preceptor, Unidade, Escala, Atendimento, Procedimento e Procedimento Realizado.

## 2. Especializacao

Pessoa e uma entidade generalizada. Paciente e Profissional sao especializacoes de Pessoa, pois ambos compartilham nome, CPF, data de nascimento, indicador `is_flamengo` e telefone.

Profissional tambem e especializado em Residente e Preceptor. A especificacao informa que um profissional pode atuar como preceptor em um periodo e como residente em outro, mantendo historico. Na Etapa 1, o papel atual e representado pelas tabelas `residente` e `preceptor`, sempre ligadas ao mesmo identificador de `profissional`.

### RestriÃ§Ãµes das especializaÃ§Ãµes

A especializaÃ§Ã£o de Pessoa em Paciente e Profissional Ã© considerada parcial
e sobreposta. Ela Ã© parcial porque uma pessoa pode ser cadastrada sem possuir
imediatamente um desses papÃ©is. Ã‰ sobreposta porque, no domÃ­nio hospitalar,
um profissional tambÃ©m pode ser atendido como paciente.

A especializaÃ§Ã£o de Profissional em Residente e Preceptor Ã© parcial e
disjunta em relaÃ§Ã£o ao papel vigente. Ã‰ parcial porque um profissional pode
ser cadastrado antes da definiÃ§Ã£o do papel. Ã‰ disjunta porque, em determinado
momento, um profissional nÃ£o pode ocupar simultaneamente os papÃ©is de
residente e preceptor.

A possibilidade de mudanÃ§a de papel ao longo do tempo pertence ao histÃ³rico
funcional. Como o modelo bÃ¡sico fornecido para a Etapa 1 nÃ£o contÃ©m datas de
inÃ­cio e fim de vigÃªncia dos papÃ©is, a implementaÃ§Ã£o atual representa apenas
o papel vigente.

## 3. Cardinalidades

- Pessoa 1:0..1 Paciente: nem toda pessoa precisa ser paciente, mas todo paciente e uma pessoa.
- Pessoa 1:0..1 Profissional: nem toda pessoa precisa ser profissional, mas todo profissional e uma pessoa.
- Profissional 1:0..1 Residente e Profissional 1:0..1 Preceptor: o papel atual do profissional e especializado.
- Paciente 1:N Atendimento: cada atendimento possui exatamente um paciente; um paciente pode ter varios atendimentos.
- Residente 1:N Atendimento: cada atendimento tem exatamente um residente responsavel.
- Preceptor 1:N Atendimento: cada atendimento tem exatamente um preceptor supervisor.
- Atendimento N:M Procedimento, resolvido por Procedimento_Realizado: um atendimento pode ter um ou mais procedimentos, e um procedimento pode ocorrer em varios atendimentos.
- Unidade 1:N Escala: cada escala pertence a uma unidade, e uma unidade possui varias escalas.
- Residente 1:N Escala e Preceptor 1:N Escala: cada plantao registra um residente e um preceptor.

## 4. Modelo relacional

- PESSOA(id_pessoa PK, nome, cpf UNIQUE, data_nascimento, is_flamengo, telefone)
- PACIENTE(id_pessoa PK/FK, num_convenio UNIQUE, alergias, grupo_sanguineo, endereco)
- PROFISSIONAL(id_pessoa PK/FK, crm UNIQUE, data_admissao, especialidade)
- RESIDENTE(id_profissional PK/FK, ano_residencia)
- PRECEPTOR(id_profissional PK/FK, titulacao)
- UNIDADE(id_unidade PK, nome UNIQUE, tipo, capacidade_leitos)
- PROCEDIMENTO(id_procedimento PK, codigo UNIQUE, nome, tempo_medio_minutos, nivel_risco)
- ATENDIMENTO(id_atendimento PK, data_hora, duracao_minutos, id_paciente FK, id_residente FK, id_preceptor FK)
- PROCEDIMENTO_REALIZADO(id_atendimento PK/FK, id_procedimento PK/FK, quantidade, tempo_real_minutos, observacao, faturado)
- ESCALA(
  id_escala PK,
  id_unidade FK,
  data_plantao,
  dia_semana,
  turno,
  id_residente FK,
  id_preceptor FK,
  UNIQUE(id_unidade, dia_semana, turno, id_residente),
  UNIQUE(id_unidade, data_plantao, turno, id_residente)
  )

## 5. Evidencia de 3FN

O modelo esta em 1FN porque todos os atributos sao atomicos. Atributos multivalorados, como procedimentos dentro de um atendimento, foram separados em `procedimento_realizado`.

O modelo esta em 2FN porque as tabelas com chave composta, especialmente `procedimento_realizado`, possuem atributos dependentes da chave completa `(id_atendimento, id_procedimento)`, e nao apenas de parte dela.

O modelo esta em 3FN porque nao ha dependencia transitiva relevante entre atributos nao chave. Dados de pessoa ficam em `pessoa`; dados especificos de paciente ficam em `paciente`; dados de procedimento ficam em `procedimento`; dados do atendimento ficam em `atendimento`. Assim, por exemplo, o nome do residente nao e repetido em `atendimento`, apenas sua FK.

## 6. Observacoes de adequacao a especificacao

A especificacao da Etapa 1 menciona atualizar endereco ou convenio do paciente, embora o diagrama textual inicial liste apenas numero do convenio, alergias e grupo sanguineo. Para atender ao CRUD solicitado, foi acrescentado o campo `endereco` em `paciente`.

A consulta de pacientes sem procedimento de risco alto exige a classificacao de risco do procedimento. Por isso, foi acrescentado `nivel_risco` em `procedimento`, com CHECK para BAIXO, MEDIO e ALTO.

A remocao de procedimento realizado depende de verificar faturamento. Por isso, foi acrescentado o campo booleano `faturado` em `procedimento_realizado`.

## 7. Ajuste operacional na tabela ESCALA

O modelo bÃ¡sico do enunciado representa uma escala pelo dia da semana.
Entretanto, a consulta analÃ­tica da Etapa 1 exige a contagem dos plantÃµes
no mÃªs corrente. Para que essa consulta pudesse ser implementada de forma
determinÃ­stica, foi acrescentado o atributo `data_plantao`.

A presenÃ§a simultÃ¢nea de `data_plantao` e `dia_semana` constitui uma
redundÃ¢ncia controlada, pois o dia da semana pode ser derivado da data.
Para impedir divergÃªncias, o schema contÃ©m a constraint
`ck_escala_data_dia_coerentes`, que valida se o valor de `dia_semana`
corresponde Ã  data informada.

O nÃºcleo do modelo permanece normalizado atÃ© a 3FN. A tabela ESCALA contÃ©m
essa desnormalizaÃ§Ã£o controlada exclusivamente para conciliar a estrutura
fornecida pelo enunciado com a consulta mensal solicitada.

## 8. LimitaÃ§Ã£o do histÃ³rico de papÃ©is na Etapa 1

A especificaÃ§Ã£o informa que um profissional pode atuar como residente em determinado perÃ­odo e como preceptor em outro. Entretanto, o modelo relacional bÃ¡sico definido para a Etapa 1 nÃ£o apresenta atributos de inÃ­cio e fim de vigÃªncia desses papÃ©is.

Por esse motivo, a implementaÃ§Ã£o atual representa somente o papel cadastrado no momento, por meio das tabelas `residente` e `preceptor`. A representaÃ§Ã£o completa do histÃ³rico exigiria uma tabela associativa com perÃ­odo de vigÃªncia ou outra estrutura adicional.

Essa extensÃ£o nÃ£o foi implementada na Etapa 1 para preservar o modelo relacional bÃ¡sico fornecido na especificaÃ§Ã£o.
