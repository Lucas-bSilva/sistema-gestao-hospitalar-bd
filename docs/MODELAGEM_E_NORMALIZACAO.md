# Modelagem e Normalizacao - Etapa 1

A implementação consegue detectar profissionais cadastrados simultaneamente
como residente e preceptor por meio de uma consulta de validação presente em
`sql/06_validacoes.sql`.

Entretanto, com a estrutura de especialização baseada exclusivamente em
tabelas separadas, uma constraint CHECK não consegue consultar a outra tabela.
Assim, a exclusividade entre os papéis não é garantida de forma preventiva
nesta etapa.

A garantia automática poderá ser implementada posteriormente por uma trigger,
por um atributo discriminador de papel vigente ou por uma tabela histórica
com períodos de vigência. Para a Etapa 1, a equipe preservou o modelo
relacional fornecido no enunciado e documentou essa limitação.

## 1. Entidades principais

O projeto representa o Hospital Universitario Dra. Yuska Maritan Brito com as entidades Pessoa, Paciente, Profissional, Residente, Preceptor, Unidade, Escala, Atendimento, Procedimento e Procedimento Realizado.

## 2. Especializacao

Pessoa e uma entidade generalizada. Paciente e Profissional sao especializacoes de Pessoa, pois ambos compartilham nome, CPF, data de nascimento, indicador `is_flamengo` e telefone.

Profissional tambem e especializado em Residente e Preceptor. A especificacao informa que um profissional pode atuar como preceptor em um periodo e como residente em outro, mantendo historico. Na Etapa 1, o papel atual e representado pelas tabelas `residente` e `preceptor`, sempre ligadas ao mesmo identificador de `profissional`.

### Restrições das especializações

A especialização de Pessoa em Paciente e Profissional é considerada parcial
e sobreposta. Ela é parcial porque uma pessoa pode ser cadastrada sem possuir
imediatamente um desses papéis. É sobreposta porque, no domínio hospitalar,
um profissional também pode ser atendido como paciente.

A especialização de Profissional em Residente e Preceptor é parcial e
disjunta em relação ao papel vigente. É parcial porque um profissional pode
ser cadastrado antes da definição do papel. É disjunta porque, em determinado
momento, um profissional não pode ocupar simultaneamente os papéis de
residente e preceptor.

A possibilidade de mudança de papel ao longo do tempo pertence ao histórico
funcional. Como o modelo básico fornecido para a Etapa 1 não contém datas de
início e fim de vigência dos papéis, a implementação atual representa apenas
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

O modelo básico do enunciado representa uma escala pelo dia da semana.
Entretanto, a consulta analítica da Etapa 1 exige a contagem dos plantões
no mês corrente. Para que essa consulta pudesse ser implementada de forma
determinística, foi acrescentado o atributo `data_plantao`.

A presença simultânea de `data_plantao` e `dia_semana` constitui uma
redundância controlada, pois o dia da semana pode ser derivado da data.
Para impedir divergências, o schema contém a constraint
`ck_escala_data_dia_coerentes`, que valida se o valor de `dia_semana`
corresponde à data informada.

O núcleo do modelo permanece normalizado até a 3FN. A tabela ESCALA contém
essa desnormalização controlada exclusivamente para conciliar a estrutura
fornecida pelo enunciado com a consulta mensal solicitada.

## 8. Limitação do histórico de papéis na Etapa 1

A especificação informa que um profissional pode atuar como residente em determinado período e como preceptor em outro. Entretanto, o modelo relacional básico definido para a Etapa 1 não apresenta atributos de início e fim de vigência desses papéis.

Por esse motivo, a implementação atual representa somente o papel cadastrado no momento, por meio das tabelas `residente` e `preceptor`. A representação completa do histórico exigiria uma tabela associativa com período de vigência ou outra estrutura adicional.

Essa extensão não foi implementada na Etapa 1 para preservar o modelo relacional básico fornecido na especificação.