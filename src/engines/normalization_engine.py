"""ETAPA 1: Normalização dos dados"""

import pandas as pd
from pathlib import Path
from typing import List, Dict, Any
from ..models.schemas import APIData


class NormalizationEngine:
    """Responsável por normalizar dados de entrada"""

    @staticmethod
    def load_csv(file_path: Path) -> pd.DataFrame:
        """Carrega CSV com separador ;"""
        df = pd.read_csv(file_path, sep=';')

        # Renomeia colunas para padrão interno
        column_mapping = {
            'sigla': 'sigla',
            'nome_api': 'nome_api',
            'volumetria media mensal': 'volumetria',
            'tempo medio resposta (ms)': 'tempo_ms',
            'tx erro medio': 'tx_erro',
            'dias new para pre preleased': 'dias_new_pre',
            'dias pre released para released': 'dias_pre_rel'
        }
        df = df.rename(columns=column_mapping)
        return df

    @staticmethod
    def normalize_api(row: pd.Series) -> APIData:
        """Normaliza uma API:
        - Converte tempo para float
        - Converte erro (% string) para float
        - Converte volumetria para float
        """
        # Trata tempo (pode vir com vírgula)
        tempo = str(row['tempo_ms']).replace(',', '.')

        # Trata erro (remove % e converte)
        erro = str(row['tx_erro']).replace('%', '').replace(',', '.')

        return APIData(
            sigla=str(row['sigla']).strip(),
            nome_api=str(row['nome_api']).strip(),
            volumetria=float(row['volumetria']),
            tempo_ms=float(tempo),
            tx_erro=float(erro),
            dias_new_pre=int(row['dias_new_pre']),
            dias_pre_rel=int(row['dias_pre_rel'])
        )

    def process(self, csv_path: Path) -> List[APIData]:
        df = self.load_csv(csv_path)
        apis = [self.normalize_api(row) for _, row in df.iterrows()]
        return apis