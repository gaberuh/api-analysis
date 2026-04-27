"""Estatística descritiva + detecção de outliers por IQR"""

from typing import List, Dict, Any
import numpy as np

FIELDS = {
    'tempo_medio_resposta_ms': 'Latência (ms)',
    'tx_erro_medio': 'Taxa de Erro (%)',
    'custo_mensal_brl': 'Custo Mensal (R$)',
    'custo_desperdicio_brl': 'Desperdício (R$)',
    'volumetria_media_mensal': 'Volumetria',
}


def compute(apis: List[Dict[str, Any]]) -> Dict[str, Any]:
    result = {}

    for field, label in FIELDS.items():
        values = np.array([a[field] for a in apis if field in a], dtype=float)
        if len(values) == 0:
            continue

        q1, q2, q3 = np.percentile(values, [25, 50, 75])
        iqr = q3 - q1
        outlier_floor = q1 - 1.5 * iqr
        outlier_ceil = q3 + 1.5 * iqr
        outliers = [a['api_name'] for a in apis if a.get(field, 0) > outlier_ceil]

        # Classifica cada API em banda de quartil
        quartile_bands: Dict[str, str] = {}
        for a in apis:
            v = a.get(field, 0)
            if v > outlier_ceil:
                band = 'OUTLIER'
            elif v > q3:
                band = 'ALTO'
            elif v > q2:
                band = 'MÉDIO_ALTO'
            elif v > q1:
                band = 'MÉDIO_BAIXO'
            else:
                band = 'BAIXO'
            quartile_bands[a['api_name']] = band

        result[field] = {
            'label': label,
            'count': int(len(values)),
            'mean': round(float(np.mean(values)), 4),
            'median': round(float(np.median(values)), 4),
            'std': round(float(np.std(values, ddof=1)), 4) if len(values) > 1 else 0.0,
            'min': round(float(np.min(values)), 4),
            'max': round(float(np.max(values)), 4),
            'q1': round(float(q1), 4),
            'q2': round(float(q2), 4),
            'q3': round(float(q3), 4),
            'iqr': round(float(iqr), 4),
            'outlier_threshold_superior': round(float(outlier_ceil), 4),
            'outlier_threshold_inferior': round(float(max(0, outlier_floor)), 4),
            'outliers': outliers,
            'outliers_count': len(outliers),
            'quartile_bands': quartile_bands,
        }

    return result
