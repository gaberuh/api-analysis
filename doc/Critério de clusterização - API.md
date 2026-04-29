# Como os clusters de APIs são definidos

Para facilitar a priorização e tomada de decisão, as APIs são agrupadas em clusters estratégicos.  
Cada cluster representa um tipo específico de problema (ou oportunidade), combinando risco operacional, impacto financeiro e relevância para o negócio.

Essa classificação não é subjetiva — ela segue critérios objetivos baseados em dados reais de uso, custo e qualidade.
## Lógica geral de clusterização

Cada API é avaliada em três dimensões principais:

Risco operacional → estabilidade (latência, erro, maturidade)  
Impacto financeiro → custo total e desperdício  
Relevância operacional → volume de uso e tipo (interna vs externa)

A partir disso, as APIs são agrupadas em clusters com regras claras.

## Resumo executivo

CRÍTICAS DE NEGÓCIO → risco externo (cliente)  
GARGALO OPERACIONAL → risco interno
CUSTO ALTO → impacto financeiro  
QUALIDADE EM RISCO → dívida técnica  
ESTÁVEL → operação saudável  
LONG TAIL → baixo impacto

## CRÍTICAS DE NEGÓCIO

### O que são:
APIs externas com alto risco.

### Como o sistema define:

API é externa  
E possui risco ALTO ou CRÍTICO

### Interpretação de negócio:
Essas APIs impactam diretamente o cliente final ou parceiros.  
Se falham, o problema é visível fora da empresa.

### Leitura executiva:
Risco reputacional + impacto direto no cliente  
Prioridade máxima

## GARGALO OPERACIONAL

### O que são:
APIs com baixa maturidade (instáveis no ciclo de desenvolvimento).

### Como o sistema define:

APIs com maturidade classificada como PROBLEMA ou CRÍTICO

### Interpretação de negócio:
São APIs que ainda não amadureceram, podem quebrar em deploy, gerar retrabalho e instabilidade.

### Leitura executiva:
Risco interno de engenharia  
Afeta velocidade de entrega e estabilidade

## CUSTO ALTO

### O que são:
APIs que concentram grande parte do custo da operação.

### Como o sistema define:

APIs classificadas com custo ALTO ou CRÍTICO (comparadas entre si)

### Interpretação de negócio:
Poucas APIs representam grande parte do gasto.

### Leitura executiva:
Onde está o dinheiro  
Melhor ponto para otimização financeira

## QUALIDADE EM RISCO

### O que são:
APIs internas com problemas relevantes de qualidade.

### Como o sistema define:

API é interna  
E possui risco ALTO ou CRÍTICO

### Interpretação de negócio:
Não impactam diretamente o cliente externo, mas afetam o funcionamento interno do sistema.

### Leitura executiva:
Dívida técnica ativa  
Pode virar problema maior se não tratado

## ESTÁVEL

### O que são:
APIs saudáveis e com uso relevante.

### Como o sistema define:

Risco BAIXO ou MÉDIO  
Volume acima do mínimo

### Interpretação de negócio:
Funcionam bem e têm uso significativo.

### Leitura executiva:
Operação saudável  
Manter e monitorar

## LONG TAIL

### O que são:
APIs com baixo uso e baixo risco.

### Como o sistema define:

Volume baixo  
E risco BAIXO ou MÉDIO

### Interpretação de negócio:
APIs pouco utilizadas e que não apresentam problemas relevantes.

### Leitura executiva:
Baixo impacto  
Candidatas a simplificação ou descontinuação



