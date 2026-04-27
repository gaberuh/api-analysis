"""ETAPA 3: Cálculo de Custo (cost_model.md)"""

from typing import Dict, Any, List
import numpy as np
from ..models.enums import NivelRisco
from ..models.schemas import APIData
from ..core.config import (
    AWS_API_GATEWAY, AWS_LAMBDA_REQUEST, AWS_LAMBDA_EXECUTION_PER_MS,
    AWS_RDS, TAXA_CAMBIO, PERCENTIL_CRITICO, PERCENTIL_ALTO,
    AWS_ALB, AWS_AUTH
)


class CostEngine:
    """Calcula custo AWS e classifica (cost_model.md)"""

    @classmethod
    def custo_unitario_usd(cls, tempo_ms: float) -> float:
        """cost_model.md #4 - Fórmula total por request"""
        lambda_exec = tempo_ms * AWS_LAMBDA_EXECUTION_PER_MS
        return AWS_API_GATEWAY + AWS_LAMBDA_REQUEST + lambda_exec + AWS_RDS + AWS_RDS + AWS_ALB + AWS_AUTH

    @classmethod
    def calculate_for_api(cls, api: APIData) -> Dict[str, Any]:
        """Calcula todos os custos para uma API"""
        custo_unit = cls.custo_unitario_usd(api.tempo_ms)

        custo_mensal_usd = api.volumetria * custo_unit
        custo_mensal_brl = custo_mensal_usd * TAXA_CAMBIO

        requests_com_erro = api.volumetria * (api.tx_erro / 100)
        custo_desperdicio_brl = requests_com_erro * custo_unit * TAXA_CAMBIO

        return {
            'sigla': api.sigla,
            'custo_unitario_usd': round(custo_unit, 10),
            'custo_mensal_usd': round(custo_mensal_usd, 2),
            'custo_mensal_brl': round(custo_mensal_brl, 2),
            'custo_desperdicio_brl': round(custo_desperdicio_brl, 2),
            'requests_com_erro': int(requests_com_erro)
        }

    @classmethod
    def classify_costs(cls, todos_custos: List[Dict]) -> Dict[str, NivelRisco]:
        """Classifica custo baseado em percentil (cost_model.md #8)"""
        if not todos_custos:
            return {}

        if len(todos_custos) == 1:
            return {todos_custos[0]['sigla']: NivelRisco.NORMAL}

        custos = [c['custo_mensal_brl'] for c in todos_custos]
        p_critico = np.percentile(custos, PERCENTIL_CRITICO)
        p_alto = np.percentile(custos, PERCENTIL_ALTO)

        classificacoes = {}
        for custo_data in todos_custos:
            custo = custo_data['custo_mensal_brl']
            if custo >= p_critico:
                classificacoes[custo_data['sigla']] = NivelRisco.CRITICO
            elif custo >= p_alto:
                classificacoes[custo_data['sigla']] = NivelRisco.ALTO
            else:
                classificacoes[custo_data['sigla']] = NivelRisco.NORMAL

        return classificacoes
