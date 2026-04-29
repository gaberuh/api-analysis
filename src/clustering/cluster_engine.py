"""ETAPA 12: Clusterização Determinística (workflow)"""

from typing import List, Dict, Any
from ..models.enums import *
from ..models.schemas import APIAnalysis
from ..core.config import VOLUMETRIA_THRESHOLDS


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
    def cluster_long_tail(analises: List[APIAnalysis]) -> List[APIAnalysis]:
        """workflow etapa 12: volumetria < limiar BAIXO AND risco ≤ MÉDIO"""
        vol_limiar = VOLUMETRIA_THRESHOLDS[0]
        return [
            a for a in analises
            if a.volumetria_media_mensal < vol_limiar and a.risco_final in ["BAIXO", "MÉDIO"]
        ]

    @staticmethod
    def cluster_qualidade_em_risco(analises: List[APIAnalysis]) -> List[APIAnalysis]:
        """APIs internas com risco ALTO ou CRÍTICO não capturadas por outros clusters.
        Sinalizam problemas de qualidade (performance/erro) que exigem atenção técnica."""
        return [a for a in analises if a.tipo == "interna" and a.risco_final in ["ALTO", "CRÍTICO"]]

    @staticmethod
    def cluster_estavel(analises: List[APIAnalysis]) -> List[APIAnalysis]:
        """APIs saudáveis (risco BAIXO ou MÉDIO) com volume acima do limiar BAIXO.
        Não são candidatas ao LONG_TAIL mas também não demandam intervenção."""
        vol_minimo_medio = VOLUMETRIA_THRESHOLDS[0]  # 1_000
        return [
            a for a in analises
            if a.risco_final in ["BAIXO", "MÉDIO"] and a.volumetria_media_mensal >= vol_minimo_medio
        ]

    @classmethod
    def generate_all_clusters(cls, analises: List[APIAnalysis]) -> Dict[str, Any]:
        """Gera todos os clusters com metadados financeiros e de risco"""
        total_cost = sum(a.custo_mensal_brl for a in analises) or 1.0

        # Clusters operacionais exigem tráfego real: APIs sem volumetria não podem
        # ser gargalo, críticas de negócio ou custo alto — só são elegíveis para LONG_TAIL.
        com_volume = [a for a in analises if a.volumetria_media_mensal > 0]

        grupos = {
            "CRÍTICAS_DE_NEGÓCIO":  cls.cluster_criticas_negocio(com_volume),
            "GARGALO_OPERACIONAL":  cls.cluster_gargalo_operacional(com_volume),
            "CUSTO_ALTO":           cls.cluster_custo_alto(com_volume),
            "QUALIDADE_EM_RISCO":   cls.cluster_qualidade_em_risco(com_volume),
            "ESTÁVEL":              cls.cluster_estavel(com_volume),
            "LONG_TAIL":            cls.cluster_long_tail(analises),
        }

        return {name: cls._enrich(apis, total_cost) for name, apis in grupos.items()}

    @staticmethod
    def _enrich(apis: List[APIAnalysis], total_cost: float) -> Dict[str, Any]:
        custo = sum(a.custo_mensal_brl for a in apis)
        desperdicio = sum(a.custo_desperdicio_brl for a in apis)
        scores = [a.score for a in apis]

        return {
            'api_names': [a.api_name for a in apis],
            'siglas': [a.sigla for a in apis],
            'count': len(apis),
            'custo_total_brl': round(custo, 2),
            'desperdicio_total_brl': round(desperdicio, 2),
            'score_medio': round(sum(scores) / len(scores), 2) if scores else 0.0,
            'score_maximo': max(scores) if scores else 0.0,
            'participacao_custo_pct': round(custo / total_cost * 100, 1),
        }
