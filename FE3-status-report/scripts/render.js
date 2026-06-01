async function loadContent() {
  const res = await fetch('./data/content.json');
  return res.json();
}

function renderHeader(meta) {
  return `
    <header class="header">
      <div class="header__eyebrow">${meta.eyebrow}</div>
      <div class="header__title">${meta.title}</div>
      <div class="header__subtitle">${meta.subtitle}</div>
      <div class="header__date">${meta.date}</div>
    </header>`;
}

function renderKPIs(diagnostico) {
  const cards = diagnostico.kpis.map(kpi => `
    <div class="kpi-card">
      <div class="kpi-card__value">${kpi.value}</div>
      <div class="kpi-card__label">${kpi.label}</div>
      <div class="kpi-card__sublabel">${kpi.sublabel}</div>
    </div>`).join('');

  return `
    <section class="kpis">
      <div class="section-header">
        <div class="section-header__accent" style="background:var(--color-orange-primary)"></div>
        <div class="section-header__title">${diagnostico.sectionTitle}</div>
      </div>
      <div class="kpis__grid">${cards}</div>
    </section>`;
}

function renderScoreBar(score, max) {
  const pct = Math.round((score / max) * 100);
  return `
    <div class="score-cell">
      <div class="score-bar-track">
        <div class="score-bar-fill" style="width:${pct}%"></div>
      </div>
      <div class="score-value">${score.toFixed(2)}</div>
    </div>`;
}

function renderAPITable(critico) {
  const rows = critico.apis.map((api, i) => {
    const rowBg = i % 2 === 0 ? 'var(--color-off-white)' : 'var(--color-white)';
    const extBadge = api.ext ? `<span class="api-table__ext-badge">EXT</span>` : '';
    return `
      <tr style="background:${rowBg}">
        <td class="api-table__rank">${api.rank}</td>
        <td class="api-table__name">${api.name}${extBadge}</td>
        <td>${renderScoreBar(api.score, api.scoreMax)}</td>
        <td>${api.erro}</td>
        <td>${api.latencia}</td>
        <td>${api.volumetria}</td>
      </tr>`;
  }).join('');

  return `
    <div class="api-table-wrapper">
      <div class="api-table__header-bar">
        <div class="api-table__header-title">${critico.sectionTitle}</div>
        <div class="api-table__header-right">
          <span class="badge-critico">${critico.badge}</span>
          <span class="api-table__cost">${critico.totalCost}</span>
        </div>
      </div>
      <table class="api-table">
        <thead>
          <tr>${critico.tableHeaders.map(h => `<th>${h}</th>`).join('')}</tr>
        </thead>
        <tbody>${rows}</tbody>
      </table>
      <div class="api-table__legend">${critico.extLegend}</div>
    </div>`;
}

function renderCorrelacoes(correlacoes) {
  const cards = correlacoes.items.map(item => `
    <div class="correlacao-card">
      <div class="correlacao-card__tag">${item.tag}</div>
      <div class="correlacao-card__title">${item.title}</div>
      <div class="correlacao-card__body">${item.body}</div>
      <div class="correlacao-card__action">${item.action}</div>
    </div>`).join('');

  return `
    <div class="correlacoes-panel">
      <div class="section-header correlacoes-panel__header">
        <div class="section-header__accent" style="background:var(--color-orange-medium)"></div>
        <div class="section-header__title">${correlacoes.sectionTitle}</div>
      </div>
      ${cards}
    </div>`;
}

function renderDiagnostico(critico, correlacoes) {
  return `
    <section class="diagnostico">
      <div class="diagnostico__body">
        ${renderAPITable(critico)}
        ${renderCorrelacoes(correlacoes)}
      </div>
    </section>`;
}

function renderSimulacao(simulacao) {
  const renderRows = (col, colorClass) =>
    col.items.map(item => `
      <div class="sim-row">
        <div class="sim-row__label">${item.percentual}</div>
        <div class="sim-row__bar-track">
          <div class="sim-row__bar-fill ${colorClass}" style="width:${item.barPercent}%"></div>
        </div>
        <div class="sim-row__value ${colorClass}">${item.value}</div>
      </div>`).join('');

  return `
    <section class="simulacao">
      <div class="section-header">
        <div class="section-header__accent" style="background:var(--color-blue-primary)"></div>
        <div class="section-header__title">${simulacao.sectionTitle}</div>
      </div>
      <div class="simulacao__grid">
        <div class="sim-col">
          <div class="sim-col__title">${simulacao.latencia.label}</div>
          ${renderRows(simulacao.latencia, '')}
        </div>
        <div class="sim-col">
          <div class="sim-col__title">${simulacao.erros.label}</div>
          ${renderRows(simulacao.erros, 'sim-row__bar-fill--blue')}
        </div>
      </div>
      <div class="simulacao__insight">${simulacao.insight}</div>
    </section>`;
}

function renderClusters(clusters) {
  const cards = clusters.items.map(item => `
    <div class="cluster-card">
      <div class="cluster-card__title">${item.title}</div>
      <div class="cluster-card__metric">${item.metric}</div>
      <div class="cluster-card__body">${item.body}</div>
      <div class="cluster-card__action">${item.action}</div>
    </div>`).join('');

  return `
    <section class="clusters">
      <div class="section-header">
        <div class="section-header__accent" style="background:var(--color-orange-primary)"></div>
        <div class="section-header__title">${clusters.sectionTitle}</div>
      </div>
      <div class="clusters__grid">${cards}</div>
    </section>`;
}

function renderScore(scoreMetodologia) {
  const cards = scoreMetodologia.criterios.map(c => `
    <div class="score-card">
      <div class="score-card__title">${c.title}</div>
      <div class="score-card__metric">${c.metric}</div>
      <div class="score-card__body">${c.body}</div>
      <div class="score-card__threshold">${c.threshold}</div>
    </div>`).join('');

  return `
    <section class="score">
      <div class="section-header">
        <div class="section-header__accent" style="background:var(--color-blue-medium)"></div>
        <div class="section-header__title">${scoreMetodologia.sectionTitle}</div>
      </div>
      <div class="score__grid">${cards}</div>
      <div class="score__formula">${scoreMetodologia.formula}</div>
    </section>`;
}

function renderRoadmap(roadmap) {
  const featureCards = roadmap.features.map(f => `
    <div class="feature-card">
      <div class="feature-card__title">
        <span class="emoji">${f.icon}</span>
        ${f.title}
      </div>
      <div class="feature-card__body">${f.body}</div>
    </div>`).join('');

  const milestones = roadmap.milestones.map(m => `
    <div class="milestone-card">
      <div class="milestone-card__header">
        <div class="milestone-card__id">${m.id}</div>
        <div class="milestone-card__header-text">
          <span class="milestone-card__period">${m.period}</span>
          <span class="milestone-card__title">${m.title}</span>
        </div>
      </div>
      <div class="milestone-card__items">
        ${m.items.map(i => `<div class="milestone-card__item">${i}</div>`).join('')}
      </div>
      <div class="milestone-card__kpi">${m.kpi}</div>
    </div>`).join('');

  return `
    <section class="roadmap">
      <div class="section-header">
        <div class="section-header__accent" style="background:var(--color-orange-primary)"></div>
        <div class="section-header__title">${roadmap.sectionTitle}</div>
      </div>
      <div class="roadmap__body">
        <div class="roadmap__features">${featureCards}</div>
        <div class="roadmap__milestones">${milestones}</div>
      </div>
    </section>`;
}

function renderCTA(cta) {
  const stats = cta.stats.map((stat, i) => {
    const divider = i > 0 ? `<div class="cta__divider"></div>` : '';
    return `${divider}
      <div class="cta-stat">
        <div class="cta-stat__value">${stat.value}</div>
        <div class="cta-stat__label">${stat.label}</div>
      </div>`;
  }).join('');

  return `
    <div class="cta">
      <div class="cta__headline">${cta.headline}</div>
      <div class="cta__subline">${cta.subline}</div>
      <div class="cta__stats">${stats}</div>
    </div>`;
}

function renderFooter(footer) {
  return `
    <footer class="footer-bar">
      <div class="footer-bar__left">${footer.left}</div>
      <div class="footer-bar__right">${footer.right}</div>
    </footer>`;
}

async function init() {
  const data = await loadContent();
  const app = document.getElementById('app');

  app.innerHTML = [
    renderHeader(data.meta),
    renderKPIs(data.diagnostico),
    renderDiagnostico(data.critico, data.correlacoes),
    renderSimulacao(data.simulacao),
    renderClusters(data.clusters),
    renderScore(data.scoreMetodologia),
    renderRoadmap(data.roadmap),
    renderCTA(data.cta),
    renderFooter(data.footer),
  ].join('\n');
}

init();
