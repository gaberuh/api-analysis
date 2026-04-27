"""Motor estatístico — orquestra os módulos e retorna resultado consolidado"""

from typing import Dict, Any

from ..models.schemas import OutputFinal
from .descriptive import compute as compute_descriptive
from .correlation import compute as compute_correlation
from .scenarios import compute as compute_scenarios
from .insights import generate as generate_insights


def run_statistics(resultado: OutputFinal) -> Dict[str, Any]:
    """Recebe OutputFinal em memória e retorna análise estatística completa"""
    if not resultado.ranking_completo:
        return {}

    apis = resultado.ranking_completo
    clusters = resultado.clusters or {}

    descriptive = compute_descriptive(apis)
    correlations = compute_correlation(apis)
    scenarios = compute_scenarios(apis)
    insights = generate_insights(apis, descriptive, correlations, scenarios, clusters)

    return {
        'total_apis_analisadas': len(apis),
        'descriptive_stats': descriptive,
        'correlations': correlations,
        'scenarios': scenarios,
        'insights': insights,
    }
