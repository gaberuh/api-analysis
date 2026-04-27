"""Enums e classificações do sistema"""

from enum import Enum

class TipoAPI(Enum):
    INTERNA = "interna"
    EXTERNA = "externa"

class NivelRisco(Enum):
    EXCELENTE = "EXCELENTE"
    SAUDAVEL = "SAUDÁVEL"
    NORMAL = "NORMAL"
    ATENCAO = "ATENÇÃO"
    PROBLEMA = "PROBLEMA"
    CRITICO = "CRÍTICO"
    ALTO = "ALTO"

class ScoreNivel(Enum):
    """Mapeamento Classificação → Score (workflow etapa 4)"""
    EXCELENTE = 0
    SAUDAVEL = 1
    NORMAL = 2
    ATENCAO = 3
    PROBLEMA = 4
    CRITICO = 5
    ALTO = 4

class CustoNivel(Enum):
    NORMAL = 2
    ALTO = 4
    CRITICO = 5

class RiscoFinal(Enum):
    BAIXO = "BAIXO"
    MEDIO = "MÉDIO"
    ALTO = "ALTO"
    CRITICO = "CRÍTICO"

class Acao(Enum):
    INTERVENCAO_IMEDIATA = "intervenção imediata"
    PRIORIDADE_ALTA = "priorizar próximo ciclo"
    PLANEJAR = "planejar"
    MONITORAR = "monitorar"

class Volumetria(Enum):
    BAIXO = "BAIXO"
    MEDIO = "MÉDIO"
    ALTO = "ALTO"
    MUITO_ALTO = "MUITO_ALTO"