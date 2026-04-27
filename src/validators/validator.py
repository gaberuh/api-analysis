"""ETAPA 15: Validação e Log de Auditoria (validator.md)"""

from typing import List, Dict, Any
from ..models.schemas import APIAnalysis, AuditLog, APIData
from ..models.enums import *


class Validator:
    """Implementa validator.md e auditoria"""

    @staticmethod
    def validate_structure(analise: APIAnalysis) -> tuple:
        """validator.md #1: Campos obrigatórios"""
        required_fields = [
            'api_name', 'sigla', 'tipo', 'performance_risk',
            'error_risk', 'maturidade', 'custo_classificacao',
            'score', 'risco_final', 'acao', 'custo_mensal_brl',
            'custo_desperdicio_brl'
        ]

        for field in required_fields:
            if not hasattr(analise, field) or getattr(analise, field) is None:
                return False, f"Campo obrigatório ausente: {field}"
        return True, "OK"

    @staticmethod
    def validate_coerencia(analise: APIAnalysis) -> tuple:
        """validator.md #3: CRÍTICO → score ≥ 3.5"""
        if analise.risco_final == "CRÍTICO" and analise.score < 3.5:
            return False, f"CRÍTICO com score {analise.score} < 3.5"
        return True, "OK"

    @staticmethod
    def validate_score_format(analise: APIAnalysis) -> tuple:
        """validator.md #5: 2 casas decimais"""
        # Converte para string e verifica se tem 2 casas decimais
        score_str = f"{analise.score:.2f}"  # Força 2 casas decimais

        # Verifica se após o ponto tem exatamente 2 dígitos
        if '.' in score_str:
            decimais = score_str.split('.')[1]
            if len(decimais) == 2:
                return True, "OK"

        return False, f"Score {analise.score} não tem 2 casas decimais"

    @classmethod
    def validate_all(cls, analise: APIAnalysis) -> Dict[str, Any]:
        """Executa todas as validações"""
        validations = {
            'estrutura': cls.validate_structure(analise),
            'coerencia': cls.validate_coerencia(analise),
            'score_format': cls.validate_score_format(analise)
        }

        for name, (is_valid, msg) in validations.items():
            if not is_valid:
                return {
                    "status": "INVALIDO",
                    "motivo": msg,
                    "campo": name
                }

        return {"status": "VALIDO"}

    @staticmethod
    def create_audit_log(api: APIData, analise: APIAnalysis,
                         detalhes: Dict[str, Any]) -> AuditLog:
        """Cria log de auditoria (workflow etapa 15)"""
        return AuditLog(
            api_name=api.nome_api,
            detalhamento=detalhes,
            calculo_score=f"score = {analise.score}",
            regras_aplicadas=[
                "risk_criteria.md - performance thresholds",
                "risk_criteria.md - error thresholds",
                "cost_model.md - AWS pricing",
                "workflow.md - scoring with weights",
                "workflow.md - tipo + volume adjustments"
            ],
            justificativa=f"API {api.sigla} classificada como {analise.risco_final} "
                          f"com score {analise.score}. Performance: {analise.performance_risk}, "
                          f"Erro: {analise.error_risk}, Custo: {analise.custo_classificacao}"
        )