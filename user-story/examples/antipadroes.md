# Anti-padrões — O que não fazer

## Anti-padrão 1: Persona de usuário final

❌ **Errado:**
> **EU, COMO** analista do POF, quero visualizar o score da conta contábil para entender sua saúde.

✅ **Correto:**
> **EU, COMO** engenheiro de dados da squad RessonâncIA, quero implementar o endpoint de consulta de score por conta contábil...

**Por quê:** Histórias de usuário final pertencem à Feature. A história aqui é para o team member construir a solução.

---

## Anti-padrão 2: Corpo em bloco único de texto

❌ **Errado:**
> O pipeline deve calcular o score sobre as seis dimensões definidas. Para cada conta processada, o resultado persistido deve incluir o score final ponderado. O pipeline deve suportar recálculo configurável. O resultado deve ser idempotente.

✅ **Correto:**
> O pipeline deve calcular o score sobre as seis dimensões definidas: completude do produto (25%), rastreabilidade (20% e 10%), modernidade tecnológica (15%), volume (10%), tempestividade (10%) e governança (10%).
>
> Para cada conta processada, o resultado persistido deve incluir o score final ponderado, o valor de cada dimensão, os pesos utilizados e a data de referência dos dados consumidos.
>
> O resultado deve ser idempotente para o mesmo conjunto de dados de entrada — reprocessar não deve gerar duplicatas.

**Por quê:** Cada bloco temático merece seu próprio parágrafo. Texto corrido dificulta leitura e revisão no refinamento.

---

## Anti-padrão 3: Critérios de aceite vagos ou sem os critérios negativos

❌ **Errado:**
> - Sistema funcionando corretamente.
> - Performance adequada.
> - Código limpo.

✅ **Correto:**
> - Score calculado para 100% das contas do conjunto de dados de entrada, sem contas ignoradas silenciosamente.
> - Latência total de processamento inferior a 30 minutos por execução.
> - Não criar código monolítico — separação clara de métodos e classes é obrigatória.

**Por quê:** Critérios vagos não são verificáveis. Os 4 critérios negativos padrão são obrigatórios em toda história.

---

## Anti-padrão 4: Estimativa de esforço incluída

❌ **Errado:**
> Esta história deve levar aproximadamente 2 dias de desenvolvimento.

✅ **Correto:** Não mencionar estimativa. A squad faz isso no refinamento.

---

## Anti-padrão 5: Nome de artefato técnico hardcoded sem contexto

❌ **Errado:**
> O job `jgb-glue-job-fe3-match-conciliacao-lançamento-v2` deve processar os dados.

✅ **Correto:**
> O Glue Job de conciliação de lançamento deve processar os dados.

**Por quê:** Nomes de artefatos mudam. A capacidade é o que importa na história, a menos que o nome seja fornecido explicitamente pelo PM.
