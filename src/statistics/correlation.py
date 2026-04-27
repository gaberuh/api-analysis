"""Correlação de Pearson entre variáveis de interesse"""

from typing import List, Dict, Any
from scipy import stats

PAIRS = [
    ('tempo_medio_resposta_ms', 'tx_erro_medio',       'latência vs taxa de erro'),
    ('tempo_medio_resposta_ms', 'custo_mensal_brl',    'latência vs custo'),
    ('tx_erro_medio',           'custo_mensal_brl',    'taxa de erro vs custo'),
    ('tx_erro_medio',           'custo_desperdicio_brl', 'taxa de erro vs desperdício'),
    ('volumetria_media_mensal', 'custo_mensal_brl',    'volumetria vs custo'),
    ('tempo_medio_resposta_ms', 'score',               'latência vs score de risco'),
    ('tx_erro_medio',           'score',               'taxa de erro vs score de risco'),
]


def _interpret_strength(r: float) -> str:
    a = abs(r)
    if a >= 0.7:
        return 'forte'
    elif a >= 0.4:
        return 'moderada'
    else:
        return 'fraca'


def compute(apis: List[Dict[str, Any]]) -> Dict[str, Any]:
    result = {}

    for field_a, field_b, label in PAIRS:
        valid = [(a[field_a], a[field_b]) for a in apis if field_a in a and field_b in a]
        if len(valid) < 5:
            continue

        xa, xb = zip(*valid)
        r, p = stats.pearsonr(list(xa), list(xb))
        r, p = float(r), float(p)
        direction = 'positiva' if r >= 0 else 'negativa'
        strength = _interpret_strength(r)
        significant = p < 0.05

        result[f"{field_a}_vs_{field_b}"] = {
            'label': label,
            'r': round(r, 4),
            'p_value': round(p, 4),
            'significant': significant,
            'strength': strength,
            'direction': direction,
            'interpretation': (
                f"Correlação {strength} {direction}"
                f"{' — estatisticamente significativa' if significant else ' — não significativa'}"
                f" (r={r:.2f}, p={p:.3f})"
            ),
        }

    return result
