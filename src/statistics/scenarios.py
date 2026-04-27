"""Simulação de cenários de impacto financeiro (redução de erro e latência)"""

from typing import List, Dict, Any
from ..core.config import (
    AWS_API_GATEWAY, AWS_LAMBDA_REQUEST,
    AWS_LAMBDA_EXECUTION_PER_MS, AWS_RDS,
    TAXA_CAMBIO, SCENARIO_REDUCTION_RATES,
)


def _unit_cost(tempo_ms: float) -> float:
    return AWS_API_GATEWAY + AWS_LAMBDA_REQUEST + (tempo_ms * AWS_LAMBDA_EXECUTION_PER_MS) + AWS_RDS


def compute(apis: List[Dict[str, Any]]) -> Dict[str, Any]:
    total_cost = sum(a['custo_mensal_brl'] for a in apis)
    total_waste = sum(a['custo_desperdicio_brl'] for a in apis)

    error_scenarios: Dict[str, Any] = {}
    latency_scenarios: Dict[str, Any] = {}

    for rate in SCENARIO_REDUCTION_RATES:
        key = f"reducao_{int(rate * 100)}pct"

        # Cenário 1: redução da taxa de erro
        # O desperdício é proporcional à tx_erro, então saving = desperdicio * rate
        saving_error = round(total_waste * rate, 2)
        error_scenarios[key] = {
            'reducao_aplicada_pct': int(rate * 100),
            'economia_mensal_brl': saving_error,
            'novo_desperdicio_total_brl': round(total_waste - saving_error, 2),
            'pct_desperdicio_recuperado': round(saving_error / total_waste * 100, 1) if total_waste > 0 else 0.0,
        }

        # Cenário 2: redução de latência
        # Recalcula custo unitário com tempo reduzido (LAMBDA_EXECUTION_PER_MS é função do tempo)
        latency_savings = []
        for api in apis:
            new_tempo = api['tempo_medio_resposta_ms'] * (1 - rate)
            new_cost = api['volumetria_media_mensal'] * _unit_cost(new_tempo) * TAXA_CAMBIO
            latency_savings.append(max(0.0, api['custo_mensal_brl'] - new_cost))

        saving_latency = round(sum(latency_savings), 2)
        latency_scenarios[key] = {
            'reducao_aplicada_pct': int(rate * 100),
            'economia_mensal_brl': saving_latency,
            'novo_custo_total_brl': round(total_cost - saving_latency, 2),
            'pct_custo_economizado': round(saving_latency / total_cost * 100, 1) if total_cost > 0 else 0.0,
            'top_apis_impactadas': _top_impacted(apis, rate),
        }

    return {
        'baseline': {
            'custo_total_brl': round(total_cost, 2),
            'desperdicio_total_brl': round(total_waste, 2),
            'pct_desperdicio': round(total_waste / total_cost * 100, 1) if total_cost > 0 else 0.0,
        },
        'reducao_erro': error_scenarios,
        'reducao_latencia': latency_scenarios,
    }


def _top_impacted(apis: List[Dict[str, Any]], rate: float, top_n: int = 5) -> List[Dict[str, Any]]:
    """Top N APIs com maior economia absoluta na redução de latência"""
    savings = []
    for api in apis:
        new_tempo = api['tempo_medio_resposta_ms'] * (1 - rate)
        new_cost = api['volumetria_media_mensal'] * _unit_cost(new_tempo) * TAXA_CAMBIO
        saving = max(0.0, api['custo_mensal_brl'] - new_cost)
        if saving > 0:
            savings.append({'api_name': api['api_name'], 'economia_brl': round(saving, 4)})

    return sorted(savings, key=lambda x: -x['economia_brl'])[:top_n]
