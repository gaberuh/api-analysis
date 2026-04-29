
Este documento descreve como os clusters são definidos a partir de regras objetivas, incluindo os limiares (thresholds) utilizados no modelo.

A clusterização é construída sobre três pilares:

- Risco operacional
- Impacto financeiro
- Volumetria (uso real)

---

## 1. Classificação base das APIs

Antes de entrar nos clusters, cada API é classificada em dimensões padronizadas.

### Volumetria (uso mensal)

A volumetria define o nível de relevância operacional da API.

**Thresholds definidos no modelo:**

- **BAIXO:** < 30 requisições/mês
- **MÉDIO:** entre 30 e 100.000
- **ALTO:** entre 100.000 e 1.000.000
- **MUITO ALTO:** > 1.000.000

**Interpretação:**

- Volumes baixos → impacto operacional reduzido
- Volumes altos → qualquer problema escala rapidamente

---

### Performance (latência)

Os limites variam por tipo de API:

**APIs internas**

- Saudável: até 700ms
- Atenção: até 1200ms
- Problema: até 2500ms
- Crítico: acima disso

**APIs externas**

- Saudável: até 500ms
- Atenção: até 800ms
- Problema: até 1200ms
- Crítico: acima disso

---

### Taxa de erro

- Excelente: < 0.1%
- Normal: < 1%
- Atenção: < 5%
- Problema: < 10%
- Crítico: ≥ 10%

**Observação importante:**  
A partir de 1% de erro, a API já entra em zona de atenção no modelo.

---

### Maturidade (estabilidade no ciclo de deploy)

Tempo entre fases do ciclo de vida:

**New → Pre-released**

- Normal: até 15 dias
- Atenção: até 30 dias
- Crítico: acima disso

**Pre-released → Released**

- Normal: até 30 dias
- Atenção: até 60 dias
- Crítico: acima disso

---

### Classificação de custo

O custo não é fixo — ele é relativo ao conjunto de APIs.

O modelo usa percentis:

- Top 10% → CRÍTICO
- Top 30% → ALTO
- Restante → NORMAL

**Importante:**  
Isso garante que sempre identificamos onde está a maior concentração de custo, mesmo com cenários diferentes.

---

## 2. Score final (base dos clusters)

Cada API recebe um score de risco de 0 a 5, baseado em:

- Performance → 30%
- Erro → 30%
- Maturidade → 15%
- Custo → 25%

**Ajustes adicionais:**

- APIs externas recebem +1 ponto (maior risco de dependência)
- APIs de alto volume recebem +1 ou +2 pontos
- Se houver qualquer dimensão crítica → o score mínimo sobe para 3.5

### Classificação final do risco

- **BAIXO:** ≤ 2.0
- **MÉDIO:** < 3.5
- **ALTO:** < 4.5
- **CRÍTICO:** ≥ 4.5

---

## 3. Regras de formação dos clusters

Agora sim — como os clusters são formados na prática.

### CRÍTICAS DE NEGÓCIO

**Critério:**

- API externa
- E risco final ALTO ou CRÍTICO

**Lógica:**  
Dependência externa + instabilidade = risco direto ao cliente

---

### GARGALO OPERACIONAL

**Critério:**

- Maturidade classificada como PROBLEMA ou CRÍTICO

**Lógica:**  
APIs que não estabilizam no ciclo de deploy → travam o fluxo de entrega

---

### CUSTO ALTO

**Critério:**

- Classificação de custo ALTO ou CRÍTICO (top 30%)

**Lógica:**  
Representam a maior parte do gasto total

---

### QUALIDADE EM RISCO

**Critério:**

- API interna
- E risco final ALTO ou CRÍTICO

**Lógica:**  
Problemas estruturais internos (latência/erro), ainda não expostos externamente

---

### ESTÁVEL

**Critério:**

- Risco BAIXO ou MÉDIO
- Volumetria ≥ 30

**Lógica:**  
APIs relevantes e saudáveis

---

### LONG TAIL

**Critério:**

- Volumetria < 30
- Risco BAIXO ou MÉDIO

**Lógica:**  
Baixo uso + baixo risco → baixo impacto

---

### Regra importante (exclusão por volumetria)

APIs com volumetria zero ou muito baixa:

- NÃO entram em clusters críticos
- Só podem cair em LONG_TAIL

**Motivo:**  
Sem uso real, não existe impacto operacional relevante

---

## Conclusão

A clusterização é baseada em:

- Thresholds claros (tempo, erro, volume)
- Classificação relativa (custo)
- Score composto (ponderado)
- Regras determinísticas (sem subjetividade)

Isso garante que:

- Dois cenários iguais sempre geram o mesmo resultado
- As decisões são explicáveis
- O modelo é auditável e escalável