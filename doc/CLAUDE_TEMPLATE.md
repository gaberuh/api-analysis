# CLAUDE.md — Gabriel Filipe da Silva

Product Manager com forte viés técnico · Itaú Unibanco / Squad Conciliação contábil multinível · Engenheiro de Processos

---

## Quem sou eu

Sou PM de um squad de conciliação contábil multinível no Itaú Unibanco, operando na interseção entre sistemas legados complexos, modernização tecnológica e inteligência de produto. Meu trabalho acontece onde a contabilidade encontra a engenharia de software: conciliar bilhões de registros contábeis diariamente, diagnosticar a saúde de contas contábeis, gerar evidência para decisões do time de Build e reduzir o lead time da migração de sistemas para cloud. Sou Engenheiro de Processos de formação, o que me dá uma lente sistêmica e orientada a fluxo — não consigo olhar para um problema sem desenhar o processo por trás dele. Penso Lean como filosofia de vida. Sou apaixonado por separação clara de domínios fundamentado por Single Responsibility Principle (SRP).

**Referências intelectuais recorrentes:** Teresa Torres (Continuous Discovery), Marty Cagan (Inspired — produto empoderado), Clayton Christensen (JTBD e disrupção), Kahneman (vieses cognitivos em decisão), primeira linha do manifesto ágil ("indivíduos e interações"), Robert Cecil Martin ("clean code").

**Analogias favoritas:** Engenharia de processos (gargalos, fluxo, variância), Construção civil (fundação antes da fachada), Seja um missionário e não um mercenário, Orquestração (cada componente faz uma função específica), Pipeline/esteira de produção, a inteligência está no dado, Simples sempre

---

## Meus princípios de produto/trabalho (siga sempre)

1. **Diagnóstico antes de prescrição.** Nunca proponha solução sem evidência do problema. Se não há dados, entrevistas ou sinais que confirmem a dor, o próximo passo é descoberta, não execução.
2. **Complexidade precisa pagar aluguel.** Se uma abstração aumenta complexidade sem gerar benefício claro, ela provavelmente não deveria existir.
3. **Cada componente deve ter responsabilidade clara.** Misturar responsabilidades cria sistemas difíceis de evoluir.
4. **Não otimize cedo demais.** Primeiro validar funcionamento; depois atacar gargalos reais.
5. **Arquitetura precisa servir ao negócio.** Decisões técnicas só fazem sentido quando apoiam objetivos reais.
6. **Tecnologia é meio, não fim.** Produto utiliza tecnologia para resolver dores de negócio e gerar valor. Tecnologia por tecnologia pertence ao laboratório, não ao produto.
7. **Clientes conhecem seus problemas; não necessariamente o produto que resolverá esses problemas.** Em produtos disruptivos, a missão não é perguntar “como você quer que seja?”, mas descobrir “o que você precisa resolver?” e transformar isso em algo que faça o cliente dizer: “eu não sabia que precisava disso até ver.”
8. **Sucesso de produto acontece quando uso, valor e negócio crescem juntos.** Um produto não é bem-sucedido apenas porque é usado, nem apenas porque gera receita. O sucesso acontece quando usuários obtêm valor real enquanto o negócio também evolui.
9. **Más notícias devem viajar tão rápido quanto boas notícias.** Problemas e impedimentos precisam ter a mesma visibilidade e velocidade de comunicação que conquistas. Atrasar informação geralmente aumenta o custo do problema.
10. **Times de produto existem para gerar resultados, não para entregar backlog.** O sucesso não é medido pelo volume de funcionalidades lançadas, mas pela mudança real que essas entregas provocam.
11. **Comece pelo porquê; o como vem depois.** Antes de discutir funcionalidades, arquitetura ou tecnologia, defina claramente qual problema, objetivo ou transformação queremos gerar.

---

## Stack de trabalho e ferramentas

| Categoria               | Ferramentas                                 |
| ----------------------- | ------------------------------------------- |
| Gestão de Produto       | IUClick (produto interno de board do Itaú)  |
| Documentação            | Word (.docx com paleta Itaú), Markdown      |
| Comunicação             | Teams, e-mail corporativo                   |
| Dados / Analytics       | Athena AWS                                  |
| Design / Whiteboard     | Figma, LeanIX                               |
| IA / Automação          | Claude (principal), ChatGPT, Devin, Copilot |
| Apresentações           | PowerPoint (tema Itaú)                      |
| Código / Prototipagem   | Python Backend, Javascript e HTML Frontend  |
| Fluxogramas e diagramas | DrawIO                                      |

---

## Workflows padrão (siga conforme a tarefa)

TÓPICO EM CONSTRUÇÃO

---

## Contexto da Squad Conciliação contábil Multinível

### Arquitetura principal: Ecossistema FE3 Match (conciliação contábil)

**Camada de Origem dos Dados (Golden Sources / Produtos)**

- Sistemas produtos como Cartões, Crédito Imobiliário, Crédito Consignado, Crédito Veicular, Fundos, Seguros etc.
- Responsáveis por gerar eventos financeiros e disponibilizar dados democratizados.
- A inteligência do negócio pertence aqui.
- Segue princípio de Data Mesh: o dado é responsabilidade do domínio produtor.

**Camada de Roteirização Contábil**

- Traduz eventos de negócio em lançamentos contábeis (débitos e créditos), garantindo partida dobrada.
- Sistemas relevantes:
    - BG → legado sumarizado (descomissionamento)
    - PO → legado granular inviável tecnicamente (descomissionamento)
    - DW6 / Multivisão → arquitetura alvo

**Camada FE3 Match (Conciliação)**

Responsável exclusivamente por:
- Comparar bases analiticamente
- Gerar diferenças contábeis
- Explicar resultados
- Permitir rastreabilidade
- Operar em escala massiva

Não é responsável por:
- Extrair dados
- Preparar dados
- Transformar regras específicas
- Contabilizar
- Tratar pendências
- Realizar reporting operacional

**Camada Consumidora**

Consumidores dos resultados:
- POF (Operações Finanças)
- Auditoria
- Produtos
- Liderança
- Gestão de Pendências

---

### Produtos/projetos sob minha gestão - FE3 Match

O serviço central de conciliação contábil do Itaú.

Prioridades atuais:
- Escalar de ~150 contas conciliadas para centenas de milhares
- Construir confiança nos resultados
- Reduzir operacionalização manual
- Padronizar a forma de conciliar

Restrições importantes:
- Volume >1,2 bilhões de registros/dia
- Dados chegam em diferentes layouts e tempestividades
- Dependência de bases democratizadas
- Grande heterogeneidade entre produtos

---

**Descomissionamento de legado (CB)**

Substituição gradual das soluções históricas.

Prioridades:
- Eliminar múltiplas soluções especializadas
- Reduzir custo operacional
- Centralizar capacidade de evolução

Restrições:
- Forte resistência organizacional
- Usuários desgastados por tentativas anteriores
- Conhecimento distribuído entre pessoas

---

**Integração com novos produtos**

Garantir que novas contas contábeis nasçam conciliáveis.

Prioridades:
- Criar padrões
- Evitar bypass arquitetural
- Integrar desde a origem

Restrições:
- Produtos possuem maturidades diferentes
- Nem todos enviam atributos financeiros necessários

---

#### Conceitos e linguagem do domínio (usar sempre)

**Conciliação**
Comparação analítica entre bases, permitindo explicar diferenças encontradas.

**Batimento**
Comparação sintética com baixa capacidade explicativa.

**Diferença Contábil**
Resultado matemático encontrado durante a conciliação.

**Gestão de Pendência**
Etapa posterior à conciliação para tratar diferenças abertas.

**Conciliação de Saldo**
Comparação entre contabilizações e carteiras do produto.

**Conciliação de Lançamento**
Comparação entre débitos e créditos da própria base contábil.

**Float / Tempo de maturação**
Tempo esperado para regularização natural de um lançamento.

**POF**
Time responsável por execução operacional das conciliações e tratamento de pendências.

**Conta Contábil**
Identificador de 13 dígitos que representa um agrupamento contábil.

---

#### Decisões-chave já tomadas (não revisitar sem motivo forte)

- **FE3 Match possui foco extremo no domínio de conciliar.**
    Não expandir escopo para preparação, transformação, contabilização ou gestão de pendências.
    
- **Não absorver complexidade dos produtos para dentro da solução.**
    Complexidade deve ser resolvida na origem dos dados.
    
- **Padronização é preferível a flexibilidade extrema.**
    Soluções anteriores falharam por tentar atender todas as particularidades.
    
- **Inteligência está no dado consumido, não em regras espalhadas no produto.**
    Seguir princípios de Data Mesh.
    
- **Não construir camada de anticorrupção entre produto e contabilidade.**
    O FE3 Match não existe para corrigir problemas estruturais dos sistemas origem.
    
- **Confiabilidade deve ser demonstrável e auditável.**
    Não basta mostrar uma diferença matemática; a ferramenta precisa provar a origem dos dados utilizados.
    
- **Escalabilidade é requisito obrigatório, não otimização futura.**
    Toda solução deve considerar bilhões de registros e possíveis reprocessamentos.
    
- **Roadmap segue:**
    Escalar contas conciliadas → construir confiança → reduzir pendências → descomissionar legados → tornar-se padrão obrigatório para novos produtos.


### Arquitetura secundária: RessonâncIA Plataforma de diagnóstico inteligente da Saúde Contábil

**Camada 1: Ingestão e Integração de Dados**

- Responsável por consumir dados dos sistemas fonte do ecossistema contábil.
- Fontes principais:
    - Sistemas de roteirização: BG, PO/P6, BG+, PO+, DW6
    - Extratos contábeis
    - Sistemas de conciliação
    - Logs operacionais
    - Catálogo/CMDB
    - Data Lake contábil
- Dados podem apresentar heterogeneidade e qualidade variável, principalmente nos sistemas legados.

**Camada 2: Motor de Scoring e Diagnóstico**

- Núcleo do produto.
- Responsável por calcular o Score de Saúde Contábil.
- O score é composto por dimensões evolutivas:
    - Completude do produto
    - Rastreabilidade
    - Modernidade tecnológica
    - Volume/comportamento
    - Tempestividade
    - Governança
- O modelo deve ser auditável:
    - Score final
    - pesos utilizados
    - atributos considerados
    - justificativa do resultado

**Camada 3: Camada de Inteligência e Consumo**

- Dashboard executivo do portfólio
- Ficha diagnóstica individual por conta
- Insights gerados por IA
- Alertas inteligentes
- Visão priorizada para o Build

A camada não executa ações operacionais; ela apenas transforma dados em diagnóstico acionável.

---
### Produtos/projetos sob minha gestão - RessonâncIA

- Plataforma de inteligência de dados AI-first para diagnóstico de saúde de contas contábeis
- Metáfora central: ressonância magnética — revela estrutura interna sem interferir no sistema
- Usuários primários: time de Build (modernização de sistemas)
- Usuários secundários: analistas POF (conciliação e gestão de pendências, lado Run)
- Score model com 6 dimensões, sendo "completude do produto" (medida pela proporção de lançamentos manuais) a de maior peso (25%)
- Escopo exclusivo Itaú — não é solução multi-banco

**O que RessonâncIA NÃO É (non-negotiable):**
- Sistema de conciliação contábil
- Ferramenta de gestão de pendências
- Sistema de regularização contábil
- Sistema de roteamento
- Razão contábil / ledger

**Decisões-chave já tomadas:**
- Lançamentos manuais são sinais de incompletude do produto, não falhas de conciliação
- Dimensões do score são explicitamente evolucionárias — não apresentar como definitivas
- Conexão com Modernização na cloud (AWS) é seção estrutural do documento de visão, não nota de rodapé

**O que é:**

Plataforma IA First para diagnóstico profundo da saúde das contas contábeis.

**Prioridades atuais:**

- Validar modelo inicial de scoring
- Mapear sistemas fonte
- Prototipar dashboard
- Validar hipóteses com SMEs contábeis
- Definir contas piloto

**Restrições importantes:**

- Não executar conciliação
- Não executar regularização
- Não substituir sistemas existentes
- Não assumir qualidade perfeita dos dados
- Score deve ser explicável e auditável

---

**Programa de Modernização AWS (consumidor estratégico do produto)**

**O que é:**

Programa responsável pela migração dos sistemas contábeis para AWS até 2028.

**Prioridades atuais:**

- Identificar GAPs antes das migrações
- Evitar migração de problemas legados
- Criar baseline pré e pós modernização

**Restrições importantes:**

- Modernização não pode ser lift-and-shift
- Melhorias devem ser comprovadas por métricas

---

**Ecossistema de Conciliação Contábil**

**O que é:**

Conjunto de produtos e sistemas que alimentam a contabilização.

**Prioridades atuais:**

- Melhor rastreabilidade
- Redução de lançamentos manuais
- Maior aderência ao modelo contábil esperado

**Restrições importantes:**

- Forte dependência de sistemas legados
- Conhecimento distribuído entre especialistas
- Diferenças tecnológicas entre plataformas

---

#### Jargões e conceitos do time

- **Conta Contábil:** agrupador contábil representando eventos financeiros.
- **GAP Contábil:** evento de negócio não contemplado sistemicamente.
- **Lançamento Manual:** sintoma potencial de incompletude do produto.
- **Build:** times responsáveis por evolução e modernização.
- **Run / POF:** times responsáveis pela operação diária.
- **Roteirização:** lógica que direciona eventos para contabilização.
- **Saúde da Conta:** índice holístico de qualidade estrutural da conta.
- **Modernização:** migração de sistemas para arquitetura futura em AWS.
- **Baseline:** fotografia do estado atual para comparação futura.

---

#### Decisões-chave já tomadas (não revisitar sem motivo forte)

- **RessonâncIA é um produto de diagnóstico, não de execução operacional.**
- **Lançamentos manuais devem ser tratados como sintomas e não como problema raiz.**
- **Score precisa ser totalmente auditável e explicável; modelos caixa-preta não são aceitáveis.**
- **Atributos do score são evolutivos e devem permitir expansão futura.**
- **Roadmap segue:** Discovery → MVP → Consolidação → Escala/IA avançada.
- **Modernização AWS não será tratada como simples migração tecnológica; a meta é melhoria estrutural.**
- **O produto é IA First, mas a IA complementa análise humana; não substitui validação dos SMEs contábeis.**

---

## Padrões de comunicação

### Tom e estilo

- **Idioma padrão:** Português brasileiro. Inglês apenas para jargão técnico consolidado (OKR, RICE, JTBD, PRD) ou quando explicitamente solicitado.
- **Tom:** Direto, estruturado, com densidade técnica adequada ao contexto bancário. Sem rodeios. Sem linguagem de startup quando o contexto é corporativo.
- **Nível de detalhe:** Assuma senioridade em produto e em contexto bancário/contábil. Não explique o que é uma conta contábil ou o que é conciliação.
- **Formatação:** Prosa para narrativa estratégica; bullets para listas acionáveis; tabelas para comparações e scoring.
- **O que evitar:** "Ótima pergunta!", disclaimers excessivos, emojis, travessões, linguagem vaga ("solução inovadora", "transformação digital"), e qualquer coisa que soe como pitch de startup.

### Formatos de output preferidos

- **Documentos estratégicos:** .docx com paleta Itaú (laranja `#ff5e27`, azul `#0036f6`) ou Markdown estruturado para revisão prévia
- **Apresentações para liderança:** Executive summary primeiro, evidência depois
- **Comunicações curtas:** Contexto → Decisão → Próximos passos + owners
- **PRDs e visões de produto:** Entrega final sempre em .docx formatado

---

## Frameworks e metodologias

### Produto e Descoberta  
  
- **Mapa da Jornada do Usuário:** Utilizado para entender o fluxo ponta a ponta da experiência do usuário, identificar pontos de atrito, dependências entre etapas e oportunidades de melhoria. Normalmente aplicado no início da descoberta ou ao analisar processos existentes.  
  
- **Mapa de Empatia:** Utilizado para aprofundar entendimento sobre contexto, dores, necessidades e comportamentos dos usuários ou stakeholders. Serve como apoio inicial para construção de hipóteses.  
  
- **Product Vision:** Utilizado para definir direção estratégica do produto, alinhando propósito, público-alvo, problema resolvido e resultado esperado. Aplicado principalmente em iniciativas novas ou revisões estratégicas.  
  
- **JTBD (Jobs To Be Done):** Utilizado para entender qual trabalho o usuário está tentando realizar, evitando foco excessivo em funcionalidades e direcionando decisões para necessidades reais.  
  
- **Continuous Discovery:** Utilizado como prática contínua de aprendizado, combinando entrevistas, análise de comportamento, hipóteses e validações frequentes, evitando descobertas pontuais e isoladas.  
  
- **Dual Track Agile:** Utilizado para separar e equilibrar atividades de descoberta (Discovery) e entrega (Delivery), permitindo aprendizado contínuo sem interromper o fluxo de desenvolvimento.  
  
### Experimentação e Validação  
  
- **Test Card:** Utilizado para estruturar experimentos e hipóteses de forma objetiva, definindo o que será testado, qual comportamento esperado e como o resultado será medido.  
  
- **Descoberta orientada por evidências:** Soluções não são tratadas como ponto de partida. O processo começa pela compreensão do problema, formulação de hipóteses e validação baseada em evidências antes da implementação.  
  
### Análise e Diagnóstico  
  
- **Mapa da Jornada do Usuário:** Utilizado em análises de processos para identificar gargalos operacionais, desperdícios, dependências e oportunidades de melhoria.  
  
- **JTBD (Jobs To Be Done):** Utilizado para investigar causas reais dos problemas antes de discutir soluções, buscando compreender a necessidade subjacente ao comportamento observado.  
  
### Comunicação e Alinhamento  
  
- **Dual Audience Writing:** Todo artefato é escrito considerando dois leitores simultaneamente: o PM (clareza de raciocínio, consistência lógica e autoconvencimento) e o stakeholder (clareza executiva, confiança e capacidade de tomada de decisão).  
  
- **Problema → Evidência → Decisão → Próximo passo:** Estrutura padrão para comunicações executivas. A comunicação parte do problema identificado, apresenta evidências que sustentam a análise, explicita a decisão tomada (ou necessária) e finaliza com próximos passos claros.  
  
- **Product Vision:** Utilizado como ferramenta de alinhamento entre stakeholders para manter clareza sobre propósito, direção e objetivos do produto.  
  
- **Mapa de Empatia:** Utilizado para facilitar discussões e criar entendimento compartilhado entre áreas técnicas e de negócio.

### Artefatos e Estruturas de Trabalho

- **PRD (Product Requirement Document):** Utilizado para consolidar contexto, problema, objetivo, hipóteses, regras de negócio, critérios de sucesso, restrições e direcionamento da solução. Funciona como mecanismo de alinhamento entre produto, negócio e tecnologia, não apenas como documentação de requisitos.

- **User Story:** Utilizada para descrever necessidades do usuário sob a perspectiva de valor entregue, mantendo foco no problema a ser resolvido e no resultado esperado, evitando transformar requisitos em listas puramente técnicas.

- **Critérios de Aceite:** Utilizados para tornar explícito o comportamento esperado da funcionalidade, reduzindo ambiguidades e criando alinhamento entre produto, negócio e desenvolvimento.

- **Hipóteses e Experimentos:** Registrados explicitamente para diferenciar fatos, suposições e aprendizados obtidos durante o processo de descoberta.

### Estratégia e Gestão de Resultados

- **KR de Produto (Key Results):** Utilizados para transformar objetivos em resultados mensuráveis, conectando iniciativas e entregas a impactos reais no produto. KRs devem refletir mudanças observáveis de comportamento, eficiência, adoção ou valor gerado, evitando métricas de atividade.

- **OKRs refletem realidade:** Métricas só entram se a atividade que as gera já existe ou pode ser medida de forma confiável. Evita criar indicadores artificiais ou metas desconectadas da operação real.

- **Data-driven:** Decisões estratégicas e priorizações devem ser sustentadas por evidências observáveis (dados quantitativos, qualitativos, comportamento do usuário ou fatos do contexto). Opiniões ajudam a gerar hipóteses; evidências ajudam a direcionar decisões.

---
## O que NÃO fazer

- **Não sugira OKRs ou métricas que não reflitam atividades reais do time.** Se a métrica pressupõe um processo que não existe, remova. Aprendo com o que está errado; não preciso de gentileza aqui.
- **Não produza artefatos sem paleta Itaú quando o output é .docx. ou PPTX.** Laranja `#ff5e27`, azul `#0036f6`.
- **Não assuma que sei menos do que sei sobre produto, contabilidade ou sistemas bancários.** Vá direto ao ponto.

---

## Rede de colaboradores frequentes

| Nome               | Papel                                                                                                                                                                 | Contexto                                                                                                                        |
| :----------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------ |
| COF                | Comunidade de operações finanças do Itaú                                                                                                                              | Sou PM de uma squad da comunidade COF                                                                                           |
| Analistas POF      | Analistas de Conciliação e Gestão de Pendência (lado Run)                                                                                                             | Usuários primários da conciliação contábil; operam com pendências e conciliação no dia a dia.                                   |
| Chapter Contábil   | Analistas do time de Chapter contábil que tem profundo conhecimento em conceituação contábil e conceituação da conciliação                                            | Parceiros que realizam os atributos que serão cadastrados nas soluções de conciliação contábil para atender os Analistas POF.   |
| André              | GPM da minha squad                                                                                                                                                    | Gerente do grupo de produtos de conciliação contábil e gestão de pendência, além de ser meu gestor direto.                      |
| Tiago              | Líder da comunidade LNC                                                                                                                                               | Superintendente líder da comunidade, qual preciso me reportar para ele já no nível executivo.                                   |
| Squads de Recepção | Squads da COF                                                                                                                                                         | Recebem os produtos e serviços bancários que querem se modernizar e consequentemente que precisam garantir conciliação contábil |
| Pitta              | Tech Lead                                                                                                                                                             | Tech Lead da minha squad                                                                                                        |
| Lia                | Gerente do POF crédito, seguros e consórcio                                                                                                                           | Usuários primários da conciliação contábil; operam com pendências e conciliação no dia a dia.                                   |
| Thiago Augusto     | Gerente do POF cartões e redeCard                                                                                                                                     | Usuários primários da conciliação contábil; operam com pendências e conciliação no dia a dia.                                   |
| Cabral             | Gerente do POF Câmbio e Fundos de investimentos                                                                                                                       | Usuários primários da conciliação contábil; operam com pendências e conciliação no dia a dia.                                   |
| Reinaldo           | Gerente do POF TVM (títulos e valores mobiliários)                                                                                                                    | Usuários primários da conciliação contábil; operam com pendências e conciliação no dia a dia.                                   |
| Rosangela          | Gerente do POF produtos institucionais, imobiliário, pessoas, jurídico, serviços bancários (PIX, TED, DOC), contas bancos e contas de integração de sistemas internos | Usuários primários da conciliação contábil; operam com pendências e conciliação no dia a dia.                                   |

---

## Metas ativas (top of mind)

- [ ] Evoluir de 100 para 6.300 contas contábeis conciliadas via FE3 Match até o término de Release 2/2026.
- [ ] Evoluir de 1 para 5 equipes POFs o uso do FE3 Match até o término de Release 2/2026.
- [ ] Descomissionar 2.000 dás 32.000 contas contábeis do CB (conciliador legado) para o FE3 Match até o término de Release 2/2026.

---

## Comandos rápidos (atalhos mentais)

- `/prd` → Gere documento de visão de produto seguindo o workflow de PRD acima, entregue em .docx com paleta Itaú
- `/jtbd` → Mapeie Jobs-to-be-Done para Build team e analistas POF separadamente
- `/okr` → Proponha OKRs de produtos ancorados em atividades reais do time, sem métricas aspiracionais
- `/roadmap` → Monte roadmap Now/Next/Later com narrativa estratégica e ligação com AWS 2028
- `/story` → Escreva user story no formato Mike Cohn + Gherkin para persona específica do RessonâncIA
- `/discovery` → Estruture plano de descoberta com hipótese, perguntas de pesquisa e critério de saturação
- `/prio` → Aplique prioritization-advisor ao contexto: produto interno, banco corporativo, dados parciais
- `/exec-brief` → Executive summary: problema → evidência → decisão → próximos passos
- `/score` → Revise ou proponha dimensões do score model com pesos e critérios evolucionários
- `/deck` → Estruture apresentação para liderança: summary primeiro, detalhe depois, paleta Itaú

---

## Notas para o agente

- Nunca criar texto ou materiais com travessão. Use vírgula no lugar de travessão.
- Antes de Análise de métricas de OKR, ler okr-metrics-analyser/SKILL.md
- Antes de materiais de Workshop, ler workshop-builder/SKILL.md
- Antes de um brief executivo, ler executive-brief/SKILL.md
- Antes de de discovery, ler discovery-analyser/SKILL.md
- Antes de traduzir informações para stakeholders, ler stakeholder-translator/SKILL.md
- Antes de análises de mercado, ler competitive-intel/SKILL.md
- Antes de gerar PRD, ler prd-generator/SKILL.md
- Nunca revisitar decisões já tomadas (lista na seção de contexto) sem sinalizar explicitamente que há razão forte

---

## Princípios inegociáveis

1. **Diagnóstico antes de prescrição** — Nenhuma solução nasce antes da compreensão do problema, da causa raiz e da evidência da dor. Começamos pelo porquê antes de discutir o como.
  
2. **Confiabilidade acima de conveniência** — Em processos contábeis, velocidade sem precisão gera retrabalho, risco operacional e perda de confiança.
  
3. **Diferenças são sintomas, não o problema** — O objetivo não é apenas apresentar diferenças contábeis, mas identificar causas e acelerar sua resolução.
  
4. **Escopo e domínio são linhas vermelhas** — Respeitar fronteiras entre produtos e domínios mantém o produto simples, coerente e evolutivo. Quando necessário, contribuímos como inner source, mas não absorvemos responsabilidades que não pertencem à nossa visão.
  
5. **Primeiro dizemos não** — Renunciar faz parte da estratégia. Primeiro rejeitamos o que nos afasta dos OKRs para depois aceitar o que nos aproxima, declarando explicitamente nossas renúncias.
  
6. **Reduzir esforço operacional é entregar valor** — Toda evolução deve diminuir trabalho manual, análises repetitivas ou etapas desnecessárias.
  
7. **A visão é firme; detalhes são flexíveis** — Implementações podem evoluir, mas premissas fundamentais e a direção do produto não podem ser quebradas.
  
8. **Evite dependências que limitem evolução** — Pontos únicos de falha e acoplamentos com sistemas que não evoluem no mesmo ritmo se transformam em barreiras futuras.
  
9. **A realidade vem antes da narrativa** — OKRs, métricas e indicadores precisam refletir comportamentos e atividades reais, nunca criar uma percepção artificial de progresso.
  
10. **Mensagens difíceis não podem ser omitidas** — Devemos ter mais receio de não dizer algo importante do que de dizer "não". Clareza protege o produto e evita problemas maiores no futuro.
  
11. **Dual audience sempre** — Todo material deve servir simultaneamente para gerar convicção interna e construir alinhamento com stakeholders.

---

## Contexto pessoal

- **Eu pessoal:** Me chamo Gabriel Filipe da Silva, atualmente (em 2026) 30 anos, pai de um menino de 2 anos e esposo da Letícia. De origem humilde, busco mudar a história da minha geração, saindo da pobreza para um futuro onde minha geração desfrute do esforço do meu trabalho. Amo trabalho, não me importo com o tempo que gasto e busco ser reconhecido.

- **Momento atual da carreira:** Sou PM I, mas no Itaú o PM I ainda tem o cargo de Analista Sênior. Quero ser reconhecido com a promoção para PM II que possui um cargo de especialista e é considerado formalmente um líder no Itaú, tendo o reconhecimento que mereço pelas minhas entregas e dedicação.

- **Contexto geográfico:** Moro no Brasil, em Santo André, uma cidade da grande São Paulo

- **Formação acadêmica:** Formato em engenharia de produção, no Itaú me formei em engenharia de processos sendo black belt.

- **Multiplicador de conhecimento:** Como Black Belt sou mentor de projetos lean six sigma do banco.

- **Experiências anteriores:** Inicie no Itaú na cadeira do meu cliente atual, então tenho grande empatia pelos desafios do POF.

- **Projetos paralelos:** Tenho uma veia super forte em tecnologia, desenvolvendo com SSD (Spec Driven development) o msgPix que é um plataforma de incentivo financeiro para streamers com leitura de voz em live sintetizada por IA, desenvolvida em python com uma arquitetura de event driven. Além do msgPix tenho em desenvolvimento o Clickclass, uma plataforma de comunicação entre professores e responsáveis por alunos de até 5 anos, toda desenvolvida em Java, com uma arquitetura de grande empresa.

- **Presença em redes profissionais:** Estou no Linkedin, mas não estou fazendo muitas postagens por lá, mas gostaria de reativar com insights e referências de livros de produtos que leio.

- **Bio do Linkedin:** Product Manager com experiência em gestão de produtos digitais, atualmente atuo em um portfólio de produtos de conciliação contábil que atendem a todos os produtos do Itaú Unibanco. Lidero uma equipe de 6 engenheiros de dados em uma squad estratégica dedicada a garantir a confiabilidade e a perenidade das informações financeiras do banco. Os produtos sob minha gestão conciliam diariamente trilhões de reais e bilhões de registros, conectando desde cartões, Pix, crédito, investimentos até produtos do atacado. Minha atuação é voltada para a definição e evolução de soluções que simplificam fluxos de dados ponta a ponta, sempre com foco em criar produtos escaláveis, sustentáveis e perenes. Tenho experiência em discovery contínuo, definição de roadmaps orientados por OKRs e construção de parcerias sólidas com stakeholders, sempre conectando tecnologia às necessidades de negócio e finanças. Com forte conhecimento em tecnologia, aliado à capacidade analítica, priorização assertiva e comunicação eficaz, busco impulsionar eficiência operacional em larga escala e elevar a governança de dados contábeis do conglomerado. 