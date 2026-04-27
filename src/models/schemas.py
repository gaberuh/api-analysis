"""Schemas de dados (Pydantic)"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from .enums import *

class APIData(BaseModel):
    """Dados brutos de uma API"""
    sigla: str
    nome_api: str
    volumetria: float
    tempo_ms: float
    tx_erro: float
    dias_new_pre: int
    dias_pre_rel: int

    class Config:
        frozen = True

class APIAnalysis(BaseModel):
    """Resultado da análise de uma API (output_schema.md)"""
    api_name: str
    sigla: str
    tipo: str
    performance_risk: str
    error_risk: str
    maturidade: str
    custo_classificacao: str
    score: float
    reliability_score: float
    efficiency_score: float
    perfil_combinado: str
    risco_final: str
    acao: str
    custo_mensal_brl: float
    custo_desperdicio_brl: float
    volumetria_media_mensal: float
    tempo_medio_resposta_ms: float
    tx_erro_medio: float
    dias_new_para_pre_released: int
    dias_pre_released_para_released: int

class AuditLog(BaseModel):
    """Log de auditoria (output_schema.md)"""
    api_name: str
    detalhamento: Dict[str, Any]
    calculo_score: str
    regras_aplicadas: List[str]
    justificativa: str

class OutputExecutivo(BaseModel):
    """Output executivo completo"""
    top_10_apis: List[APIAnalysis]
    impacto_financeiro_total: float
    desperdicio_total: float
    principais_riscos: List[str]

class OutputFinal(BaseModel):
    status: str
    executivo: Optional[Dict[str, Any]] = None
    ranking_completo: Optional[List[Dict[str, Any]]] = None
    visao_por_sigla: Optional[Dict[str, Any]] = None
    clusters: Optional[Dict[str, Any]] = None
    detalhamento: Optional[List[Dict[str, Any]]] = None
    auditoria: Optional[List[Dict[str, Any]]] = None
    statistics: Optional[Dict[str, Any]] = None
    erro: Optional[str] = None