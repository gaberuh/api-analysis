"""Score de Confiabilidade e Score de Eficiência — dimensões independentes do score final"""

from ..models.enums import NivelRisco

# Espelha ScoringEngine.RISCO_TO_SCORE — definido localmente para evitar acoplamento entre engines
_RISCO_TO_SCORE = {
    NivelRisco.EXCELENTE: 0,
    NivelRisco.SAUDAVEL: 1,
    NivelRisco.NORMAL: 2,
    NivelRisco.ATENCAO: 3,
    NivelRisco.PROBLEMA: 4,
    NivelRisco.ALTO: 4,
    NivelRisco.CRITICO: 5,
}

# Limiar a partir do qual o score é considerado "alto" na matriz 2x2 (60% do máximo)
_LIMIAR_ALTO = 3.0


class ScoreComponentsEngine:
    """Calcula Reliability Score e Efficiency Score como dimensões independentes.

    Ambos os scores seguem a mesma escala do score_base (0–5, maior = pior),
    mantendo consistência com o modelo existente sem alterar o final_score.
    """

    @classmethod
    def calculate_reliability_score(
        cls,
        performance_risk: NivelRisco,
        error_risk: NivelRisco,
        maturidade: NivelRisco,
    ) -> float:
        """Risco operacional — responde: 'essa API compromete a estabilidade do sistema?'

        Pesos: performance 40%, erro 40%, maturidade 20%.
        Enfatiza latência e erro por serem os principais drivers de instabilidade.
        """
        perf = _RISCO_TO_SCORE.get(performance_risk, 2)
        error = _RISCO_TO_SCORE.get(error_risk, 2)
        mat = _RISCO_TO_SCORE.get(maturidade, 2)
        return round(perf * 0.40 + error * 0.40 + mat * 0.20, 2)

    @classmethod
    def calculate_efficiency_score(
        cls,
        custo_nivel: NivelRisco,
        custo_mensal_brl: float,
        custo_desperdicio_brl: float,
    ) -> float:
        """Impacto financeiro — responde: 'essa API consome recursos de forma ineficiente?'

        Pesos: classificação de custo 60%, proporção de desperdício 40%.
        O desperdício relativo (erro/custo) captura ineficiência independente do volume absoluto.
        """
        cost_score = _RISCO_TO_SCORE.get(custo_nivel, 2)
        waste_ratio = custo_desperdicio_brl / custo_mensal_brl if custo_mensal_brl > 0 else 0
        waste_score = min(waste_ratio * 5, 5)
        return round(cost_score * 0.60 + waste_score * 0.40, 2)

    @classmethod
    def classify_combined(cls, reliability_score: float, efficiency_score: float) -> str:
        """Matriz 2×2: perfil combinado de confiabilidade vs eficiência.

        CRÍTICO   — instável e caro (prioridade máxima)
        INSTÁVEL  — risco operacional alto, custo aceitável
        ONEROSO   — estável, mas financeiramente ineficiente
        SAUDÁVEL  — sem alertas relevantes em nenhuma dimensão
        """
        alto_risco_op = reliability_score >= _LIMIAR_ALTO
        alto_risco_fin = efficiency_score >= _LIMIAR_ALTO

        if alto_risco_op and alto_risco_fin:
            return "CRÍTICO"
        elif alto_risco_op:
            return "INSTÁVEL"
        elif alto_risco_fin:
            return "ONEROSO"
        return "SAUDÁVEL"
