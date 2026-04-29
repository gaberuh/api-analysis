import os
import logging
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


BASE_DIR = Path(__file__).parent.parent.parent

DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"

for dir_path in [DATA_DIR, OUTPUT_DIR, LOGS_DIR]:
    dir_path.mkdir(exist_ok=True)

# Configuração de logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FILE = LOGS_DIR / "app.log"

# Mapeamento string para nível de logging
LOG_LEVEL_MAP = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}

def setup_logger(name: str = "api_analyzer") -> logging.Logger:
    """Configura e retorna um logger padronizado"""

    logger = logging.getLogger(name)

    # Evita duplicação de handlers
    if logger.handlers:
        return logger

    logger.setLevel(LOG_LEVEL_MAP.get(LOG_LEVEL, logging.INFO))

    # Formato do log
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Handler para arquivo (tudo)
    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Handler para console (apenas WARNING e ERROR)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

TAXA_CAMBIO = 5.0
PERCENTIL_CRITICO = 90
PERCENTIL_ALTO = 70

# Pesos do score (workflow etapa 5)
SCORE_WEIGHTS = {
    "performance": 0.30,
    "erro": 0.30,
    "maturidade": 0.15,
    "custo": 0.25
}

# AWS Pricing (cost_model.md #1-3)
AWS_API_GATEWAY = 0.0000035           # $ por request
AWS_LAMBDA_REQUEST = 0.0000002        # $ por request
AWS_LAMBDA_EXECUTION_PER_MS = 0.0000000021  # $ por ms
AWS_RDS = 0.000002                  # $ por request
AWS_ALB = 0.0000015       # load balancer diluído
AWS_AUTH = 0.000001       # JWT / authorizer médio


# Performance thresholds em ms (risk_criteria.md #2) - (saudavel, atencao, problema)
PERF_INTERNA = (700, 1200, 2500)
PERF_EXTERNA = (500, 800, 1200)

# Error rate thresholds em % (risk_criteria.md #3) - (excelente, normal, atencao, problema)
ERROR_THRESHOLDS = (0.1, 1.0, 5.0, 10.0)

# Volumetria thresholds (risk_criteria.md #4) - (baixo<, medio<=, alto<=)
VOLUMETRIA_THRESHOLDS = (30, 100_000, 1_000_000)

# Maturidade thresholds em dias (risk_criteria.md #6) - (normal, atencao)
MATURIDADE_NEW_PRE = (15, 30)
MATURIDADE_PRE_REL = (30, 60)

# Score classification thresholds (workflow etapa 9) - (baixo, medio, alto)
SCORE_THRESHOLDS = (2.0, 3.5, 4.5)

# Ajuste de score por volumetria (workflow etapa 6)
VOLUME_ADJUST = {'ALTO': 1, 'MUITO_ALTO': 2}

# Ajuste de score por tipo externo (workflow etapa 6)
TIPO_EXTERNA_ADJUST = 1

# Pesos para score agregado por SIGLA
SIGLA_PIOR_PESO = 0.7
SIGLA_MEDIO_PESO = 0.3

# Taxas de redução para simulação de cenários (scenarios.py)
SCENARIO_REDUCTION_RATES = [0.10, 0.20, 0.30]