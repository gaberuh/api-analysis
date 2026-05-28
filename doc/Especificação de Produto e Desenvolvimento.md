# FE3 Match, Monitoramento Saldo Zero

## Objetivo do documento

Este documento tem como objetivo especificar a feature “Monitoramento Saldo Zero” do ecossistema FE3 Match.

A especificação deve permitir que uma IA gere um MVP funcional seguindo os princípios de Spec Driven Development (SDD), preservando:

- clareza de domínio
- responsabilidades bem definidas
- separação arquitetural
- foco em escalabilidade
- aderência ao contexto contábil do FE3 Match

---

# Contexto de negócio

No contexto da conciliação contábil do Itaú Unibanco, existem aproximadamente 67 mil contas contábeis classificadas como “Saldo Zero”.

Essas contas:

- possuem saldo contábil zerado
- não possuem movimentação contábil há meses
- ainda precisam ser monitoradas operacionalmente
- continuam sob responsabilidade do POF

Mesmo sem diferenças contábeis ou movimentações, a ausência prolongada de movimentação é uma informação operacional relevante e precisa ser acompanhada.

Hoje não existe uma visão consolidada e especializada dessas contas.

---

# Problema

Os analistas e gestores POF não possuem:

- visibilidade centralizada das contas classificadas como saldo zero
- rastreabilidade operacional dessas contas
- identificação rápida de contas que voltaram a receber movimentação
- capacidade analítica para acompanhar volume, aging e distribuição das contas

Isso gera:

- acompanhamento manual
- baixa visibilidade operacional
- dificuldade de priorização
- risco operacional quando uma conta volta a movimentar sem acompanhamento

---

# Objetivo da feature

Criar uma funcionalidade no FE3 Match capaz de:

- monitorar contas classificadas como “Saldo Zero”
- apresentar visão analítica operacional
- alertar contas que voltaram a ter movimentação
- permitir acompanhamento pelos gestores POF
- fornecer visibilidade executiva e operacional

---

# Nome da Feature

FE3 Match - Monitoramento Saldo Zero

---

# Usuário alvo

## Usuário primário

POF

## Usuários secundários

- Gestão POF
- Liderança operacional
- Times de acompanhamento contábil

---

# Escopo da solução

A solução deve:

- exibir contas saldo zero
- mostrar há quantos meses a conta está sem movimentação
- permitir filtros operacionais
- destacar contas que voltaram a movimentar
- permitir exportação de dados
- gerar alertas operacionais (funcionalidade para o futuro pós validação do MVP))
- consumir dados especializados gerados por Glue Job

---

# Fora de escopo

A solução NÃO deve:

- realizar conciliação contábil
- tratar pendências
- permitir edição manual de dados
- cadastrar contas diretamente no frontend
- executar contabilização
- transformar regras contábeis
- possuir autenticação no MVP
- possuir backend transacional

---

# Jornada do usuário

## Fluxo principal

1. Usuário acessa painel de Monitoramento Saldo Zero
2. Usuário visualiza indicadores gerais
3. Usuário filtra contas por:
    - gestor POF
    - classificação
    - aging sem movimento
4. Usuário identifica contas críticas
5. Usuário acessa lista detalhada
6. Usuário exporta informações
7. Usuário acompanha contas que voltaram a movimentar

---

# Regras de negócio

## RN001

Uma conta saldo zero é uma conta:

- cadastrada no Portal de Conciliação
- classificada com tipo de conciliação “Saldo Zero”

## RN002

O cadastro da conta NÃO será realizado no FE3 Match.

O cadastro é responsabilidade exclusiva do Portal de Conciliação já existente.

## RN003

Uma conta deve permanecer visível mesmo sem movimentação contábil, para isso as contas cadastradas no Portal de Conciliação devem ser utilizadas como Primary Key no cruzamento, já que é esse dado que possui a relação de todas as contas contábeis, inclusive as que não tiverem movimentos contábeis ou sados.

## RN004

Caso uma conta volte a receber movimentação contábil:

- ela deve ser destacada visualmente
- deve aparecer em seção de alertas (futuro pós validação do MVP)
- deve gerar alerta via Teams para o gestor responsável (futuro pós validação do MVP)

## RN005

Mesmo que o saldo continue zerado, qualquer movimentação contábil deve ser considerada como evento relevante operacionalmente.

## RN006

A feature é exclusivamente de consulta.

Não haverá:

- inserts
- updates
- deletes

---

# Requisitos funcionais

## RF001

O sistema deve listar contas saldo zero.

## RF002

O sistema deve permitir filtro por:

- gestor responsável
- gerente POF
- classificação da conta
- quantidade de meses sem movimentação

## RF003

O sistema deve apresentar:

- número da conta
- nome da conta
- gestor responsável
- gerente POF
- classificação
- saldo contábil
- quantidade de meses sem movimentação
- status operacional

## RF004

O sistema deve possuir uma área de destaque para:  
“Contas que voltaram a possuir movimentação”.

## RF005

O sistema deve permitir exportação CSV, com base nos filtros aplicados.

## RF006

O sistema deve apresentar indicadores agregados:

- total de contas monitoradas
- quantidade de contas por gestor
- distribuição por aging
- quantidade de contas com nova movimentação

---

# Requisitos não funcionais

## RNF001

A solução deve suportar escala futura de 200 mil contas contábeis, por isso a importância do trabalho com paginação, ainda que no frontend para o MVP.

## RNF002

A arquitetura deve preservar separação clara de responsabilidades.

## RNF003

O frontend deve ser desacoplado da origem dos dados.

## RNF004

O MVP deve funcionar utilizando arquivos estáticos locais.

## RNF005

O código deve seguir clean code e SRP.

## RNF006

O frontend deve possuir organização preparada para evolução futura.

---

# Especificação da experiência frontend

---

# Objetivo do frontend

O frontend deve ser:

- extremamente simples, mas visualmente sofisticado
- altamente legível
- operacional
- orientado a consulta
- preparado para futura integração real

A interface deve priorizar:

- visibilidade operacional
- clareza dos alertas
- facilidade de filtro
- leitura rápida

---

# Estrutura esperada da tela

## Header da aplicação

Deve conter:

- nome da funcionalidade
- data de atualização dos dados
- botão de exportação CSV

---

## Área de indicadores (cards)

Deve conter cards com:

- total de contas saldo zero
- contas sem movimento há mais de 6 meses
- contas sem movimento há mais de 12 meses
- contas com nova movimentação
- quantidade de gestores monitorados

---

## Área de alertas críticos

Sessão visualmente destacada contendo:

- contas que voltaram a movimentar
- gestor responsável
- data da movimentação
- quantidade de registros encontrados

Essa sessão deve possuir:

- destaque visual forte
- prioridade visual máxima da tela

---

## Área de filtros

Filtros esperados:

- gestor responsável
- gerente POF
- classificação da conta
- aging sem movimento
- busca textual por número da conta

O filtros aplicados devem ficar visíveis e com possibilidade de remoção individual.
Aqui está o maior foco de usabilidade, já que é onde o usuário mais irá manipular.

Se possível, ainda no MVP, os filtros aplicados devem ser mantidos salvo em cookies ou seja lá onde for a melhor prática, não sendo necessário salvar nada em backend.

---

## Área principal de dados

Tabela operacional contendo:

- número da conta
- nome da conta
- gestor responsável
- gerente POF
- classificação
- saldo contábil atual
- meses sem movimentação
- status

---

# Comportamentos esperados do frontend

## Estados da aplicação

O frontend deve possuir:

- loading state
- empty state
- error state

---

## Comportamento dos alertas

Contas com nova movimentação devem:

- possuir badge visual
- aparecer no topo
- possuir destaque em cor
- possuir priorização visual

---

## Responsividade

Mesmo sendo MVP:

- a aplicação deve funcionar minimamente em resoluções menores
- priorizar desktop
- não precisa experiência mobile dedicada

---

# Fonte de dados do frontend

## MVP

O frontend NÃO consumirá APIs.

Os dados devem ser carregados via:

- arquivos JSON estáticos
- arquivos CSV estáticos

Todos os mocks devem estar centralizados em:

```
/data
```

---

# Estrutura esperada do projeto frontend

```
/frontend  /assets  /components  /pages  /services  /mocks  /styles  /utils  index.html
```

---

# Stack frontend

## Obrigatório

- HTML
- Javascript
- CSS

## Não utilizar

- frameworks complexos
- backend frontend
- autenticação
- banco de dados

---

# Backend

## Objetivo

Gerar dataset especializado para consumo do frontend.

---

# Arquitetura esperada

## Glue Job

Responsável por:

- leitura das bases
- enriquecimento
- cruzamento dos dados
- geração do output especializado

O Código do Glue Job deve ser feito em apenas um arquivo, pois para o MVP o mesmo rodará no Glue Job da conta consumer, que não aceita a separação de arquivos neste momento, porém pode e deve ser segregado por classes e domínios.

A Main deve ser simples e apenas apontar as direções, toda a responsabilidade de orquestração fica a cargo dos demais métodos e classes.

---

# Stack backend

## Obrigatório

- pySpark
- AWS Glue

---

# Premissas técnicas backend

## Performance

Mesmo sendo MVP:

- performance é obrigatória
- evitar scans desnecessários
- evitar joins custosos sem critério
- evitar collect
- evitar lógica row by row

---

# Schema esperado do output

```
numero_conta_contabildata_contabilvalor_movimentoqtde_registrosvalor_saldo_contabilnome_gestor_responsavelnome_gerente_POFnome_contaclassificacao_contameses_sem_movimentopossui_movimentacao_recente
```

---

# Tabelas origem

## RCC

### Contexto

Tabela de registros contábeis utilizada para conciliação.

### Responsabilidade

Origem dos lançamentos contábeis.

### Schema

### Endereço

### Amostra de dados

---

## Base Única

### Contexto

Base de cadastro das contas contábeis.

### Responsabilidade

Origem das informações organizacionais e cadastrais.

### Schema

### Endereço

### Amostra de dados

---

## Saldos Contábeis

### Contexto

Tabela de saldo contábil das contas.

### Responsabilidade

Origem do saldo atual da conta.

### Schema

### Endereço

### Amostra de dados

---

# Alertas Teams - Funcionalidade fora do MVP

## Objetivo

Notificar gestores responsáveis quando uma conta:

- voltar a possuir movimentação
- ainda que mantenha saldo zero

---

# Critérios de aceite

## CA001

Usuário consegue visualizar contas saldo zero.

## CA002

Usuário consegue filtrar contas.

## CA003

Usuário consegue identificar contas que voltaram a movimentar.

## CA004

Frontend funciona apenas com arquivos estáticos locais.

## CA005

Glue Job gera dataset consolidado corretamente.

## CA006

Exportação CSV funciona.

## CA007

Projeto possui organização modular, pronto para evolução e escala do MVP para produto final.

---

# Instruções globais de engenharia

## O que fazer

- utilizar padrão IDS do Itaú
- seguir SRP
- manter responsabilidades claras
- evitar acoplamento desnecessário
- estruturar projeto pensando em evolução futura
- utilizar clean code
- utilizar nomenclaturas claras
- manter arquitetura simples

---

## O que não fazer

- não criar código monolítico no frontend
- não misturar domínio com visualização
- não criar lógica excessiva na UI
- não criar dependências desnecessárias
- não comentar excessivamente
- não criar abstrações sem necessidade

---

# Dicionário do domínio

Todos os conceitos utilizados neste documento devem seguir o contexto definido no arquivo:  
`CLAUDE.md`

Especialmente:

- POF
- Conciliação
- Diferença Contábil
- Gestão de Pendência
- Conta Contábil
- FE3 Match
- Saldo Zero
- Rastreabilidade
- Build
- Run
- Data Mesh