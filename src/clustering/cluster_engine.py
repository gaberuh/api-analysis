"""ETAPA 12: Clusterização Determinística (workflow)"""

from typing import List, Dict, Any
from ..models.enums import *
from ..models.schemas import APIAnalysis


class ClusterEngine:
    """Cria clusters determinísticos baseados nas regras"""

    @staticmethod
    def cluster_criticas_negocio(analises: List[APIAnalysis]) -> List[APIAnalysis]:
        """workflow etapa 12: tipo = EXTERNA AND risco ≥ ALTO"""
        return [a for a in analises if a.tipo == "externa" and a.risco_final in ["ALTO", "CRÍTICO"]]

    @staticmethod
    def cluster_gargalo_operacional(analises: List[APIAnalysis]) -> List[APIAnalysis]:
        """workflow etapa 12: maturidade ≥ PROBLEMA"""
        return [a for a in analises if a.maturidade in ["PROBLEMA", "CRÍTICO"]]

    @staticmethod
    def cluster_custo_alto(analises: List[APIAnalysis]) -> List[APIAnalysis]:
        """workflow etapa 12: custo ≥ ALTO"""
        return [a for a in analises if a.custo_classificacao in ["ALTO", "CRÍTICO"]]

    @staticmethod
    def cluster_long_tail(analises: List[APIAnalysis], volumes: Dict[str, str]) -> List[APIAnalysis]:
        """workflow etapa 12: volumetria = BAIXO AND risco ≤ MÉDIO"""
        return [
            a for a in analises
            if volumes.get(a.sigla, "") == "BAIXO" and a.risco_final in ["BAIXO", "MÉDIO"]
        ]

    @classmethod
    def generate_all_clusters(cls, analises: List[APIAnalysis],
                              volumes: Dict[str, str]) -> Dict[str, Any]:
        """Gera todos os clusters com metadados financeiros e de risco"""
        total_cost = sum(a.custo_mensal_brl for a in analises) or 1.0

        grupos = {
            "CRÍTICAS_DE_NEGÓCIO": cls.cluster_criticas_negocio(analises),
            "GARGALO_OPERACIONAL": cls.cluster_gargalo_operacional(analises),
            "CUSTO_ALTO":          cls.cluster_custo_alto(analises),
            "LONG_TAIL":           cls.cluster_long_tail(analises, volumes),
        }

        return {name: cls._enrich(apis, total_cost) for name, apis in grupos.items()}

    @staticmethod
    def _enrich(apis: List[APIAnalysis], total_cost: float) -> Dict[str, Any]:
        custo = sum(a.custo_mensal_brl for a in apis)
        desperdicio = sum(a.custo_desperdicio_brl for a in apis)
        scores = [a.score for a in apis]

        return {
            'siglas': [a.sigla for a in apis],
            'count': len(apis),
            'custo_total_brl': round(custo, 2),
            'desperdicio_total_brl': round(desperdicio, 2),
            'score_medio': round(sum(scores) / len(scores), 2) if scores else 0.0,
            'score_maximo': max(scores) if scores else 0.0,
            'participacao_custo_pct': round(custo / total_cost * 100, 1),
        }
