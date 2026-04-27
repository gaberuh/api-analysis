import math
from decimal import Decimal, ROUND_HALF_UP
from typing import Tuple
from ..models.enums import NivelRisco, TipoAPI, Volumetria, RiscoFinal, Acao
from ..core.config import SCORE_WEIGHTS, VOLUME_ADJUST, TIPO_EXTERNA_ADJUST, SCORE_THRESHOLDS


class ScoringEngine:
    """Calcula scores e classificação final (workflow etapas 4-9)"""

    # Mapeamento Classificação → Score (workflow etapa 4)
    RISCO_TO_SCORE = {
        NivelRisco.EXCELENTE: 0,
        NivelRisco.SAUDAVEL: 1,
        NivelRisco.NORMAL: 2,
        NivelRisco.ATENCAO: 3,
        NivelRisco.PROBLEMA: 4,
        NivelRisco.ALTO: 4,
        NivelRisco.CRITICO: 5
    }

    @classmethod
    def score_base(cls, performance: NivelRisco, erro: NivelRisco,
                   maturidade: NivelRisco, custo: NivelRisco) -> float:
        """workflow etapa 5: score_base ponderado"""
        return (
            cls.RISCO_TO_SCORE.get(performance, 2) * SCORE_WEIGHTS['performance'] +
            cls.RISCO_TO_SCORE.get(erro, 2) * SCORE_WEIGHTS['erro'] +
            cls.RISCO_TO_SCORE.get(maturidade, 2) * SCORE_WEIGHTS['maturidade'] +
            cls.RISCO_TO_SCORE.get(custo, 2) * SCORE_WEIGHTS['custo']
        )

    @classmethod
    def final_score(cls, score_base: float, tipo: TipoAPI,
                    volume_nivel: Volumetria, tem_critico: bool) -> float:
        """workflow etapas 6, 7, 8: ajustes + dominância + arredondamento"""
        score = score_base

        if tipo == TipoAPI.EXTERNA:
            score += TIPO_EXTERNA_ADJUST

        score += VOLUME_ADJUST.get(volume_nivel.value, 0)

        if tem_critico:
            score = max(score, SCORE_THRESHOLDS[1])  # mínimo 3.5

        return float(Decimal(str(math.floor(score * 100 + 0.5) / 100)).quantize(
            Decimal('0.00'), rounding=ROUND_HALF_UP
        ))

    @classmethod
    def classify_final_risk(cls, score: float) -> Tuple[RiscoFinal, Acao]:
        """workflow etapa 9: Classificação Final e Ações"""
        baixo, medio, alto = SCORE_THRESHOLDS
        if score <= baixo:
            return RiscoFinal.BAIXO, Acao.MONITORAR
        elif score < medio:
            return RiscoFinal.MEDIO, Acao.PLANEJAR
        elif score < alto:
            return RiscoFinal.ALTO, Acao.PRIORIDADE_ALTA
        else:
            return RiscoFinal.CRITICO, Acao.INTERVENCAO_IMEDIATA

    @classmethod
    def get_maturidade_final(cls, risco_new_pre: NivelRisco,
                             risco_pre_rel: NivelRisco) -> NivelRisco:
        """Pega o pior nível entre as duas fases de maturidade"""
        pior_score = max(
            cls.RISCO_TO_SCORE.get(risco_new_pre, 2),
            cls.RISCO_TO_SCORE.get(risco_pre_rel, 2)
        )
        for risco, score in cls.RISCO_TO_SCORE.items():
            if score == pior_score:
                return risco
        return NivelRisco.NORMAL
