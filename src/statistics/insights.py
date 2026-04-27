"""Geração de insights executivos a partir das análises estatísticas"""

from typing import List, Dict, Any


def generate(
    apis: List[Dict[str, Any]],
    descriptive: Dict[str, Any],
    correlations: Dict[str, Any],
    scenarios: Dict[str, Any],
    clusters: Dict[str, Any],
) -> List[str]:
    insights: List[str] = []
    n = len(apis)

    _latency_insights(apis, n, descriptive, insights)
    _error_insights(apis, n, descriptive, insights)
    _cost_insights(apis, n, descriptive, scenarios, insights)
    _risk_insights(apis, n, insights)
    _correlation_insights(correlations, insights)
    _scenario_insights(scenarios, insights)
    _cluster_insights(clusters, scenarios, insights)

    return insights


# ── helpers ────────────────────────────────────────────────────────────────

def _latency_insights(apis, n, descriptive, out):
    d = descriptive.get('tempo_medio_resposta_ms')
    if not d:
        return
    above_q3 = sum(1 for a in apis if a['tempo_medio_resposta_ms'] > d['q3'])
    out.append(
        f"Latência mediana é {d['median']:.0f}ms — "
        f"{above_q3} APIs ({above_q3 / n * 100:.0f}%) estão acima do P75 ({d['q3']:.0f}ms)"
    )
    if d['outliers_count'] > 0:
        nomes = ', '.join(d['outliers'][:3])
        sufixo = f' e outras {d["outliers_count"] - 3}' if d['outliers_count'] > 3 else ''
        out.append(
            f"{d['outliers_count']} API(s) são outliers de latência (acima de {d['outlier_threshold_superior']:.0f}ms): "
            f"{nomes}{sufixo}"
        )


def _error_insights(apis, n, descriptive, out):
    d = descriptive.get('tx_erro_medio')
    if not d:
        return
    zero_error = sum(1 for a in apis if a['tx_erro_medio'] == 0)
    critical_error = sum(1 for a in apis if a['tx_erro_medio'] >= 5.0)
    above_1pct = sum(1 for a in apis if a['tx_erro_medio'] >= 1.0)

    if zero_error > 0:
        out.append(f"{zero_error} APIs ({zero_error / n * 100:.0f}%) operam com taxa de erro zero")
    if above_1pct > 0:
        out.append(
            f"{above_1pct} APIs ({above_1pct / n * 100:.0f}%) têm taxa de erro ≥1% — "
            f"limiar que aciona nível ATENÇÃO no modelo de risco"
        )
    if critical_error > 0:
        out.append(
            f"{critical_error} APIs ({critical_error / n * 100:.0f}%) com taxa de erro ≥5% — "
            f"classificadas como PROBLEMA/CRÍTICO, impacto direto no score"
        )
    if d['outliers_count'] > 0:
        out.append(
            f"{d['outliers_count']} API(s) são outliers de taxa de erro "
            f"(acima de {d['outlier_threshold_superior']:.1f}%): {', '.join(d['outliers'][:3])}"
        )


def _cost_insights(apis, n, descriptive, scenarios, out):
    baseline = scenarios.get('baseline', {})
    total_cost = baseline.get('custo_total_brl', 0)
    total_waste = baseline.get('desperdicio_total_brl', 0)
    waste_pct = baseline.get('pct_desperdicio', 0)

    if total_cost > 0:
        out.append(
            f"Custo operacional total: R${total_cost:,.2f}/mês — "
            f"R${total_waste:,.2f} ({waste_pct:.1f}%) são desperdício por requisições com erro"
        )

    # Top 3 APIs por custo
    top3 = sorted(apis, key=lambda x: -x['custo_mensal_brl'])[:3]
    top3_cost = sum(a['custo_mensal_brl'] for a in top3)
    if total_cost > 0 and top3_cost > 0:
        out.append(
            f"As 3 APIs de maior custo ({', '.join(a['sigla'] for a in top3)}) "
            f"concentram {top3_cost / total_cost * 100:.1f}% do gasto total (R${top3_cost:,.2f}/mês)"
        )

    d = descriptive.get('custo_mensal_brl')
    if d and d['outliers_count'] > 0:
        out.append(
            f"{d['outliers_count']} API(s) são outliers de custo (acima de R${d['outlier_threshold_superior']:,.2f}/mês): "
            f"{', '.join(d['outliers'][:3])}"
        )


def _risk_insights(apis, n, out):
    risk_count: Dict[str, int] = {}
    for a in apis:
        risk_count[a['risco_final']] = risk_count.get(a['risco_final'], 0) + 1

    critico = risk_count.get('CRÍTICO', 0)
    alto = risk_count.get('ALTO', 0)
    medio = risk_count.get('MÉDIO', 0)
    baixo = risk_count.get('BAIXO', 0)

    if critico + alto > 0:
        out.append(
            f"{critico + alto} de {n} APIs ({(critico + alto) / n * 100:.0f}%) requerem ação — "
            f"{critico} em CRÍTICO e {alto} em ALTO"
        )
    if medio + baixo > 0:
        out.append(
            f"{medio + baixo} APIs estão em risco controlado (MÉDIO/BAIXO) — "
            f"monitoramento de rotina suficiente"
        )

    # Custo dos críticos
    criticos_apis = [a for a in apis if a['risco_final'] == 'CRÍTICO']
    if criticos_apis:
        custo_criticos = sum(a['custo_mensal_brl'] for a in criticos_apis)
        out.append(
            f"As {len(criticos_apis)} APIs em CRÍTICO representam R${custo_criticos:,.2f}/mês em custo operacional"
        )


def _correlation_insights(correlations, out):
    strong = [(k, v) for k, v in correlations.items() if v['significant'] and abs(v['r']) >= 0.7]
    moderate = [(k, v) for k, v in correlations.items() if v['significant'] and 0.4 <= abs(v['r']) < 0.7]

    for _, corr in strong:
        out.append(f"[Correlação forte] {corr['label'].capitalize()}: {corr['interpretation']}")

    for _, corr in moderate:
        out.append(f"[Correlação moderada] {corr['label'].capitalize()}: {corr['interpretation']}")

    # Insight sobre driver de score
    score_drivers = [
        (k, v) for k, v in correlations.items()
        if '_vs_score' in k and v['significant']
    ]
    if score_drivers:
        score_drivers.sort(key=lambda x: -abs(x[1]['r']))
        top = score_drivers[0][1]
        out.append(
            f"Principal driver de score de risco: {top['label']} (r={top['r']:.2f}) — "
            f"endereçar esta variável tem maior impacto no risco calculado"
        )


def _scenario_insights(scenarios, out):
    err_20 = scenarios.get('reducao_erro', {}).get('reducao_20pct')
    lat_20 = scenarios.get('reducao_latencia', {}).get('reducao_20pct')
    lat_30 = scenarios.get('reducao_latencia', {}).get('reducao_30pct')

    if err_20 and err_20['economia_mensal_brl'] > 0:
        out.append(
            f"Reduzir taxa de erro em 20% economizaria R${err_20['economia_mensal_brl']:,.2f}/mês "
            f"({err_20['pct_desperdicio_recuperado']}% do desperdício atual)"
        )
    if lat_20 and lat_20['economia_mensal_brl'] > 0:
        out.append(
            f"Reduzir latência em 20% economizaria R${lat_20['economia_mensal_brl']:,.2f}/mês "
            f"({lat_20['pct_custo_economizado']}% do custo operacional)"
        )
    if lat_30 and lat_20:
        diff = lat_30['economia_mensal_brl'] - lat_20['economia_mensal_brl']
        if diff > 0:
            out.append(
                f"Passar de 20% para 30% de redução de latência gera adicional de "
                f"R${diff:,.2f}/mês — retorno marginal a avaliar"
            )


def _cluster_insights(clusters, scenarios, out):
    if not clusters:
        return

    total_cost = scenarios.get('baseline', {}).get('custo_total_brl', 0)

    for name, data in clusters.items():
        if not isinstance(data, dict) or data.get('count', 0) == 0:
            continue

        count = data['count']
        custo = data.get('custo_total_brl', 0)
        desperdicio = data.get('desperdicio_total_brl', 0)
        score_medio = data.get('score_medio', 0)
        participacao = data.get('participacao_custo_pct', 0)

        if name == 'CRÍTICAS_DE_NEGÓCIO' and count > 0:
            out.append(
                f"Cluster CRÍTICAS_DE_NEGÓCIO: {count} APIs externas de alto risco — "
                f"impacto direto no cliente final; custo R${custo:,.2f}/mês ({participacao:.1f}% do total)"
            )
        elif name == 'GARGALO_OPERACIONAL' and count > 0:
            out.append(
                f"Cluster GARGALO_OPERACIONAL: {count} APIs com maturidade crítica (score médio {score_medio}) — "
                f"risco de instabilidade em releases; desperdício R${desperdicio:,.2f}/mês"
            )
        elif name == 'CUSTO_ALTO' and count > 0:
            pct_waste = round(desperdicio / custo * 100, 1) if custo > 0 else 0
            out.append(
                f"Cluster CUSTO_ALTO: {count} APIs concentram R${custo:,.2f}/mês ({participacao:.1f}% do custo total) "
                f"com {pct_waste:.1f}% em desperdício por erro"
            )
        elif name == 'LONG_TAIL' and count > 0:
            out.append(
                f"Cluster LONG_TAIL: {count} APIs de baixo volume e risco controlado — "
                f"candidatas a revisão de SLA ou descomissionamento"
            )
