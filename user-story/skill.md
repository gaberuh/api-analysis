---
name: user-story
description: Gera histórias de usuário no formato da squad de conciliação contábil do Itaú (Gabriel Filipe / FE3 Match e RessonâncIA). Use SEMPRE que o usuário pedir para criar, escrever ou redigir uma história de usuário, story, US, ticket de desenvolvimento, ou quando mencionar "quero criar uma história", "me ajuda com uma story", "escreve um ticket". A história é orientada ao team member (desenvolvedor), não ao usuário final — segue o formato EU, COMO, QUERO, PARA QUE, com vínculo ao OKR ativo e critérios de aceite técnicos com critérios negativos padrão. Nunca calcular estimativa de esforço.
---

# Histórias de Usuário — Squad Conciliação Contábil Multinível (Itaú)

## Passo 0: Carregar contexto (obrigatório antes de escrever)

Antes de qualquer coisa, carregar:

1. **CLAUDE.md do Gabriel** — já disponível no contexto da conversa. Consultar a seção **"Metas ativas"** para os OKRs vigentes.
2. **Product Vision do produto da história:**
   - FE3 Match → `/mnt/project/FE3_Match_Product_Vision_v1.md`
   - RessonâncIA → `/mnt/project/RessonancIA_ProductVision_v1_0.md`
   - Se o produto não estiver explícito no pedido, ler os dois antes de perguntar.

Só escrever a história depois de ter o contexto carregado.

---

## Princípios

- Persona é sempre técnica: engenheiro de dados, engenheiro de software, analista de dados. Nunca o usuário final.
- A história deve caber em até 3 dias de trabalho. Se o escopo for maior, fracionar e alertar o PM antes de escrever.
- Nunca calcular estimativa de esforço. Isso é feito pela squad no refinamento.
- Referências a componentes técnicos usam a capacidade, não o nome do artefato — salvo quando o nome for fornecido explicitamente.
- O vínculo com o OKR é uma diretriz declarada, não um detalhe imperceptível.
- Critérios negativos padrão são sempre incluídos, sem exceção.
- Mínimo de 500 caracteres no corpo da história (exigência do Itaú).

---

## Formato obrigatório

```
### [Título curto e descritivo]

**EU, COMO** [role técnica].
**QUERO** [ação técnica orientada a um entregável concreto].
**PARA QUE** [finalidade técnica imediata que esta entrega habilita].
**CONTRIBUINDO ASSIM** com o atendimento do OKR: [OKR relevante da seção "Metas ativas" do CLAUDE.md].

[Parágrafo 1: contexto, contrato de dados ou regra principal.]

[Parágrafo 2: comportamento de fluxo, tempestividade ou integração.]

[Parágrafo 3: restrições, idempotência, rastreabilidade ou dependências.]

---

#### Critérios de Aceite

**Funcionais:**
- [critério mensurável]

**Critérios negativos:**
- Não infringir a responsabilidade do domínio específico do componente — cada serviço deve respeitar sua fronteira de responsabilidade.
- Não criar código monolítico — separação clara de métodos e classes é obrigatória.
- Não incluir comentários desnecessários no código — o código deve ser autoexplicativo.
- Não implantar em produção sem teste integrado e sincronização com os demais serviços da aplicação.
```

**Regras de formatação do corpo:**
- Um parágrafo por bloco temático. Nunca um bloco único de texto corrido.
- Cada parágrafo termina com ponto final.
- O corpo complementa os critérios de aceite — não duplica.

---

## Alertas obrigatórios

**História grande demais:** Sinalizar antes de escrever: "Este escopo sugere mais de 3 dias de desenvolvimento. Recomendo fracionar em [N] histórias. Quer que eu faça isso agora?"

**OKR não identificável:** Perguntar antes de escrever: "Não consegui mapear esta história a um OKR ativo. Pode confirmar o produto e o objetivo estratégico que ela atende?"

**Produto não reconhecido:** Sinalizar: "Este produto não está nos arquivos de contexto disponíveis. Me dê o contexto do produto e os OKRs relevantes."

---

## Checklist antes de entregar

- [ ] CLAUDE.md e Product Vision do produto foram lidos?
- [ ] A persona é técnica?
- [ ] O escopo cabe em até 3 dias?
- [ ] O OKR está explícito e declarado?
- [ ] O corpo tem mais de 500 caracteres?
- [ ] O corpo está em parágrafos separados por bloco temático?
- [ ] Os 4 critérios negativos padrão estão presentes?
- [ ] Estimativa de esforço foi omitida?

---

## Referências

- Exemplo de história bem escrita: `examples/exemplo-fed-match.md`
- Exemplo de história mal escrita (anti-padrões): `examples/antipadroes.md`
