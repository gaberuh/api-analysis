"""ETAPA 2: Classificação Base (risk_criteria.md)"""

from typing import Tuple
from ..models.enums import NivelRisco, TipoAPI, Volumetria
from ..core.config import (
    PERF_INTERNA, PERF_EXTERNA,
    ERROR_THRESHOLDS, VOLUMETRIA_THRESHOLDS,
    MATURIDADE_NEW_PRE, MATURIDADE_PRE_REL
)


class RiskEngine:
    """Calcula riscos de performance, erro e maturidade"""

    @staticmethod
    def classify_tipo(nome_api: str) -> TipoAPI:
        """Classifica tipo baseado no nome (risk_criteria.md #1)"""
        if 'interno' in nome_api.lower():
            return TipoAPI.INTERNA
        return TipoAPI.EXTERNA

    @staticmethod
    def performance_risk(tempo_ms: float, tipo: TipoAPI) -> NivelRisco:
        """risk_criteria.md #2"""
        saudavel, atencao, problema = PERF_INTERNA if tipo == TipoAPI.INTERNA else PERF_EXTERNA
        if tempo_ms <= saudavel:
            return NivelRisco.SAUDAVEL
        elif tempo_ms <= atencao:
            return NivelRisco.ATENCAO
        elif tempo_ms <= problema:
            return NivelRisco.PROBLEMA
        else:
            return NivelRisco.CRITICO

    @staticmethod
    def error_risk(tx_erro: float) -> NivelRisco:
        """risk_criteria.md #3"""
        excelente, normal, atencao, problema = ERROR_THRESHOLDS
        if tx_erro < excelente:
            return NivelRisco.EXCELENTE
        elif tx_erro < normal:
            return NivelRisco.NORMAL
        elif tx_erro < atencao:
            return NivelRisco.ATENCAO
        elif tx_erro < problema:
            return NivelRisco.PROBLEMA
        else:
            return NivelRisco.CRITICO

    @staticmethod
    def volumetria_nivel(volume: float) -> Volumetria:
        """risk_criteria.md #4"""
        baixo, medio, alto = VOLUMETRIA_THRESHOLDS
        if volume < baixo:
            return Volumetria.BAIXO
        elif volume <= medio:
            return Volumetria.MEDIO
        elif volume <= alto:
            return Volumetria.ALTO
        else:
            return Volumetria.MUITO_ALTO

    @staticmethod
    def maturidade_risk(dias_new_pre: int, dias_pre_rel: int) -> Tuple[NivelRisco, NivelRisco]:
        """risk_criteria.md #6 - Retorna (risco_new_pre, risco_pre_rel)"""

        def classify(dias: int, thresholds: Tuple[int, int]) -> NivelRisco:
            normal, atencao = thresholds
            if dias <= normal:
                return NivelRisco.NORMAL
            elif dias <= atencao:
                return NivelRisco.ATENCAO
            else:
                return NivelRisco.CRITICO

        return classify(dias_new_pre, MATURIDADE_NEW_PRE), classify(dias_pre_rel, MATURIDADE_PRE_REL)
