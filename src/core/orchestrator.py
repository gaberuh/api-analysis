"""Pipeline de análise - orquestra os motores em 15 etapas"""

import json
from pathlib import Path
from typing import List, Dict

from .config import setup_logger, OUTPUT_DIR, SIGLA_PIOR_PESO, SIGLA_MEDIO_PESO
from ..engines.normalization_engine import NormalizationEngine
from ..engines.risk_engine import RiskEngine
from ..engines.cost_engine import CostEngine
from ..engines.scoring_engine import ScoringEngine
from ..engines.score_components_engine import ScoreComponentsEngine
from ..clustering.cluster_engine import ClusterEngine
from ..validators.validator import Validator
from ..models.schemas import APIAnalysis, OutputFinal
from ..models.enums import NivelRisco
from ..statistics.engine import run_statistics

logger = setup_logger(__name__)


def run_analysis(csv_path: Path) -> OutputFinal:
    """Pipeline completo de análise - 15 etapas"""

    logger.info("=" * 60)
    logger.info("Iniciando análise de APIs - Modo Determinístico v2.0")
    logger.info("=" * 60)

    # ETAPA 1: Normalização
    logger.info("ETAPA 1: Normalizando dados...")
    apis = NormalizationEngine().process(csv_path)
    logger.info(f"{len(apis)} APIs carregadas e normalizadas")

    # ETAPA 2-3: Classificação de riscos + cálculo de custos
    logger.info("ETAPA 2-3: Classificando riscos e calculando custos...")
    risk_engine = RiskEngine()
    cost_engine = CostEngine()

    todos_custos = []
    analises_temp = []

    for api in apis:
        tipo = risk_engine.classify_tipo(api.nome_api)
        perf_risk = risk_engine.performance_risk(api.tempo_ms, tipo)
        err_risk = risk_engine.error_risk(api.tx_erro)
        vol_nivel = risk_engine.volumetria_nivel(api.volumetria)
        risco_new_pre, risco_pre_rel = risk_engine.maturidade_risk(api.dias_new_pre, api.dias_pre_rel)
        mat_risk = ScoringEngine.get_maturidade_final(risco_new_pre, risco_pre_rel)

        custo_data = cost_engine.calculate_for_api(api)
        todos_custos.append({'sigla': api.sigla, 'custo_mensal_brl': custo_data['custo_mensal_brl']})

        analises_temp.append({
            'api': api, 'tipo': tipo,
            'perf_risk': perf_risk, 'err_risk': err_risk,
            'mat_risk': mat_risk, 'vol_nivel': vol_nivel,
            'custo_data': custo_data,
            'risco_new_pre': risco_new_pre, 'risco_pre_rel': risco_pre_rel
        })

        logger.debug(f"API {api.sigla}: perf={perf_risk.value}, err={err_risk.value}, mat={mat_risk.value}")

    custo_classificacoes = cost_engine.classify_costs(todos_custos)

    # ETAPA 4-9: Score e classificação final
    logger.info("ETAPA 4-9: Calculando scores...")
    resultados: List[APIAnalysis] = []
    volumes_dict: Dict[str, str] = {}

    for temp in analises_temp:
        custo_nivel = custo_classificacoes.get(temp['api'].sigla, NivelRisco.NORMAL)

        tem_critico = any([
            temp['perf_risk'] == NivelRisco.CRITICO,
            temp['err_risk'] == NivelRisco.CRITICO,
            temp['mat_risk'] == NivelRisco.CRITICO,
            custo_nivel == NivelRisco.CRITICO,
        ])

        score_base = ScoringEngine.score_base(temp['perf_risk'], temp['err_risk'], temp['mat_risk'], custo_nivel)
        score_final = ScoringEngine.final_score(score_base, temp['tipo'], temp['vol_nivel'], tem_critico)
        risco_final, acao = ScoringEngine.classify_final_risk(score_final)

        reliability_score = ScoreComponentsEngine.calculate_reliability_score(
            temp['perf_risk'], temp['err_risk'], temp['mat_risk']
        )
        efficiency_score = ScoreComponentsEngine.calculate_efficiency_score(
            custo_nivel,
            temp['custo_data']['custo_mensal_brl'],
            temp['custo_data']['custo_desperdicio_brl'],
        )
        perfil_combinado = ScoreComponentsEngine.classify_combined(reliability_score, efficiency_score)

        analise = APIAnalysis(
            api_name=temp['api'].nome_api,
            sigla=temp['api'].sigla,
            tipo=temp['tipo'].value,
            performance_risk=temp['perf_risk'].value,
            error_risk=temp['err_risk'].value,
            maturidade=temp['mat_risk'].value,
            custo_classificacao=custo_nivel.value,
            score=round(score_final, 2),
            reliability_score=reliability_score,
            efficiency_score=efficiency_score,
            perfil_combinado=perfil_combinado,
            risco_final=risco_final.value,
            acao=acao.value,
            custo_mensal_brl=round(temp['custo_data']['custo_mensal_brl'], 2),
            custo_desperdicio_brl=round(temp['custo_data']['custo_desperdicio_brl'], 2),
            volumetria_media_mensal=temp['api'].volumetria,
            tempo_medio_resposta_ms=temp['api'].tempo_ms,
            tx_erro_medio=temp['api'].tx_erro,
            dias_new_para_pre_released=temp['api'].dias_new_pre,
            dias_pre_released_para_released=temp['api'].dias_pre_rel,
        )

        resultados.append(analise)
        volumes_dict[temp['api'].sigla] = temp['vol_nivel'].value

        logger.debug(
            f"API {temp['api'].sigla}: score_base={score_base:.2f}, score_final={score_final:.2f}, risco={risco_final.value}"
        )

    # ETAPA 10: Ranking
    logger.info("ETAPA 10-11: Gerando ranking...")
    ranking = sorted(resultados, key=lambda x: (-x.score, -x.custo_mensal_brl))

    # ETAPA 11: Agrupamento por SIGLA
    visao_sigla = _build_visao_sigla(resultados)

    # ETAPA 12: Clusters
    logger.info("ETAPA 12: Gerando clusters...")
    clusters = ClusterEngine.generate_all_clusters(resultados, volumes_dict)

    # ETAPA 13-14: Resumo executivo
    impacto_total = sum(r.custo_mensal_brl for r in resultados)
    desperdicio_total = sum(r.custo_desperdicio_brl for r in resultados)
    riscos_contagem = {}
    for r in resultados:
        riscos_contagem[r.risco_final] = riscos_contagem.get(r.risco_final, 0) + 1

    # ETAPA 15: Validação
    logger.info("ETAPA 15: Validando...")
    for r in resultados:
        valid = Validator.validate_all(r)
        if valid['status'] == 'INVALIDO':
            logger.error(f"Validação falhou para API {r.sigla}: {valid.get('motivo')}")
            return OutputFinal(status="INVALIDO", erro=f"Validação falhou: {valid.get('motivo')}")

    logger.info("✅ Análise concluída com sucesso!")
    logger.info(f"Total de APIs analisadas: {len(resultados)}")
    logger.info(f"Impacto financeiro total: R$ {impacto_total:,.2f}")
    logger.info(f"Desperdício total: R$ {desperdicio_total:,.2f}")

    resultado = OutputFinal(
        status="VALIDO",
        executivo={
            "top_10_apis": [r.model_dump() for r in ranking[:10]],
            "impacto_financeiro_total": impacto_total,
            "desperdicio_total": desperdicio_total,
            "principais_riscos": [f"{risco}: {qtd}" for risco, qtd in riscos_contagem.items()],
            "resumo_por_risco": riscos_contagem,
            "total_apis": len(resultados),
        },
        ranking_completo=[r.model_dump() for r in ranking],
        visao_por_sigla=visao_sigla,
        clusters=clusters,
        detalhamento=[r.model_dump() for r in resultados],
    )

    # Módulo estatístico — consome OutputFinal em memória
    logger.info("ETAPA 16: Calculando estatísticas avançadas...")
    resultado.statistics = run_statistics(resultado)
    logger.info(f"  {len(resultado.statistics.get('insights', []))} insights gerados")

    return resultado


def save_analysis_outputs(resultado: OutputFinal, timestamp: str) -> None:
    """Persiste os três arquivos de saída no diretório output/"""

    analise_file = OUTPUT_DIR / f"analise_completa_{timestamp}.json"
    with open(analise_file, 'w', encoding='utf-8') as f:
        json.dump(resultado.model_dump(), f, indent=2, ensure_ascii=False)
    logger.info(f"📄 Análise completa salva em: {analise_file}")

    if resultado.status != "VALIDO" or not resultado.executivo:
        return

    executivo_dict = (
        resultado.executivo.model_dump()
        if hasattr(resultado.executivo, 'model_dump')
        else resultado.executivo
    )

    executivo_file = OUTPUT_DIR / f"relatorio_executivo_{timestamp}.json"
    with open(executivo_file, 'w', encoding='utf-8') as f:
        json.dump(executivo_dict, f, indent=2, ensure_ascii=False)
    logger.info(f"📄 Relatório executivo salvo em: {executivo_file}")

    simplificado = {
        "timestamp": timestamp,
        "status": resultado.status,
        "ranking_priorizado": [
            {"posicao": i + 1, "sigla": api["sigla"], "score": api["score"], "risco": api["risco_final"]}
            for i, api in enumerate(executivo_dict["top_10_apis"])
        ],
        "clusters": resultado.clusters,
        "impacto_total": executivo_dict["impacto_financeiro_total"],
        "desperdicio_total": executivo_dict["desperdicio_total"],
    }
    simplificado_file = OUTPUT_DIR / f"ranking_simplificado_{timestamp}.json"
    with open(simplificado_file, 'w', encoding='utf-8') as f:
        json.dump(simplificado, f, indent=2, ensure_ascii=False)
    logger.info(f"📄 Ranking simplificado salvo em: {simplificado_file}")

    if resultado.statistics:
        statistics_file = OUTPUT_DIR / f"statistics_output_{timestamp}.json"
        with open(statistics_file, 'w', encoding='utf-8') as f:
            json.dump(resultado.statistics, f, indent=2, ensure_ascii=False)
        logger.info(f"📄 Estatísticas avançadas salvas em: {statistics_file}")


def _build_visao_sigla(resultados: List[APIAnalysis]) -> Dict:
    """Agrega métricas por SIGLA (workflow etapa 11)"""
    sigla_map: Dict[str, List[APIAnalysis]] = {}
    for r in resultados:
        sigla_map.setdefault(r.sigla, []).append(r)

    visao = {}
    for sigla, analises in sigla_map.items():
        scores = [a.score for a in analises]
        score_medio = sum(scores) / len(scores)
        pior_score = max(scores)
        visao[sigla] = {
            'score_medio': round(score_medio, 2),
            'pior_score': pior_score,
            'score_sigla': round(pior_score * SIGLA_PIOR_PESO + score_medio * SIGLA_MEDIO_PESO, 2),
            'custo_total': sum(a.custo_mensal_brl for a in analises),
            'desperdicio_total': sum(a.custo_desperdicio_brl for a in analises),
            'pior_risco': max(a.risco_final for a in analises),
        }
    return visao
