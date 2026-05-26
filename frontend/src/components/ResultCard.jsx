import { formatCurrency } from "../utils/formatters"

export default function ResultCard({ result, requestData, onReset }) {
  if (!result) return null

  const score = result.score ?? result.financial_score ?? 0
  const classification = result.classification || "Diagnóstico indisponível"
  const diagnosis =
    result.diagnosis ||
    "Não foi possível detalhar o diagnóstico desta análise. Refazer a análise pode resolver o problema."
  const uniqueAlerts = [...new Set(result.alerts || [])]
  const uniqueRecommendations = [...new Set(result.recommendations || [])]

  const getTone = (score) => {
    if (score < 40) return "danger"
    if (score < 60) return "warning"
    if (score < 80) return "attention"
    return "success"
  }

  return (
    <section className="card result-card">
      <div className="section-heading">
        <span className="eyebrow">Resultado</span>
        <h2>Seu diagnóstico financeiro</h2>
      </div>

      <div className={`score-hero ${getTone(score)}`}>
        <span className="score-label">Score financeiro</span>
        <strong>{score}</strong>
      </div>

      <div className="result-meta">
        <span className={`badge ${getTone(score)}`}>{classification}</span>
      </div>

      <div className="result-copy">
        <h3>Diagnóstico</h3>
        <p>{diagnosis}</p>
      </div>

      <div className="result-copy">
        <h3>Alertas principais</h3>
        {uniqueAlerts.length > 0 ? (
          <ul>
            {uniqueAlerts.map((alert, index) => (
              <li key={`${alert}-${index}`}>{alert}</li>
            ))}
          </ul>
        ) : (
          <p>Nenhum alerta crítico foi identificado nesta análise.</p>
        )}
      </div>

      <div className="result-copy">
        <h3>Recomendações práticas</h3>
        {uniqueRecommendations.length > 0 ? (
          <ul>
            {uniqueRecommendations.map((recommendation, index) => (
              <li key={`${recommendation}-${index}`}>{recommendation}</li>
            ))}
          </ul>
        ) : (
          <p>Refaça a análise para receber recomendações personalizadas.</p>
        )}
      </div>

      {requestData ? (
        <div className="result-summary">
          <h3>Dados informados</h3>
          <dl>
            <div>
              <dt>Receita</dt>
              <dd>{formatCurrency(requestData.receita)}</dd>
            </div>
            <div>
              <dt>Despesas</dt>
              <dd>{formatCurrency(requestData.despesas)}</dd>
            </div>
            <div>
              <dt>Dívida</dt>
              <dd>{formatCurrency(requestData.divida)}</dd>
            </div>
            <div>
              <dt>Reserva</dt>
              <dd>{formatCurrency(requestData.reserva)}</dd>
            </div>
          </dl>
        </div>
      ) : null}

      <button onClick={onReset} className="secondary-button" type="button">
        Refazer análise
      </button>

      <p className="legal-note">
        Esta análise tem caráter informativo e não substitui orientação
        financeira profissional.
      </p>
    </section>
  )
}
