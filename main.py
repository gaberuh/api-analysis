#!/usr/bin/env python3
"""Ponto de entrada — aponta a rota e liga os motores"""

from pathlib import Path
from datetime import datetime

from src.core.config import setup_logger, DATA_DIR
from src.core.orchestrator import run_analysis, save_analysis_outputs

logger = setup_logger(__name__)

CSV_PATH = DATA_DIR / "apis.csv"


def main():
    if not CSV_PATH.exists():
        logger.error(f"Arquivo não encontrado: {CSV_PATH}")
        logger.info("Coloque seu CSV em data/apis.csv")
        return

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    try:
        resultado = run_analysis(CSV_PATH)
        save_analysis_outputs(resultado, timestamp)

        if resultado.status == "VALIDO" and resultado.executivo:
            logger.info("=" * 60)
            logger.info(f"Status: {resultado.status}")
            logger.info(f"Total APIs: {resultado.executivo['total_apis']}")
            logger.info(f"Impacto total: R$ {resultado.executivo['impacto_financeiro_total']:,.2f}")
            logger.info(f"Desperdício: R$ {resultado.executivo['desperdicio_total']:,.2f}")
            logger.info("=" * 60)
        else:
            logger.warning(f"Análise inválida: {resultado.erro}")

    except Exception as e:
        logger.exception(f"Erro fatal durante a execução: {e}")
        raise


if __name__ == "__main__":
    main()
