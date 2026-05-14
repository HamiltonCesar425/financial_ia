export default function ResultCard({ result, requestData, onReset }) {
  if (!result) return null;

  const uniqueAlerts = [...new Set(result.alerts)];
  const uniqueRecommendations = [...new Set(result.recommendations)];

  const formatCurrency = (value) =>
    new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
    }).format(value);

  const getTone = (score) => {
    if (score < 40) return "danger";
    if (score < 60) return "warning";
    if (score < 80) return "attention";
    return "success";
  };

  return (
    <section className="card result-card">
      <div className="section-heading">
        <span className="eyebrow">Resultado</span>
        <h2>Seu diagnóstico financeiro</h2>
      </div>

      <div className={`score-hero ${getTone(result.score)}`}>
        <span className="score-label">Score financeiro</span>
        <strong>{result.score}</strong>
      </div>

      <div className="result-meta">
        <span className={`badge ${getTone(result.score)}`}>
          {result.classification}
        </span>
      </div>

      <div className="result-copy">
        <h3>Diagnóstico</h3>
        <p>{result.diagnosis}</p>
      </div>

      <div className="result-copy">
        <h3>Alertas principais</h3>
        <ul>
          {uniqueAlerts.map((alert, index) => (
            <li key={`${alert}-${index}`}>{alert}</li>
          ))}
        </ul>
      </div>

      <div className="result-copy">
        <h3>Recomendações práticas</h3>
        <ul>
          {uniqueRecommendations.map((recommendation, index) => (
            <li key={`${recommendation}-${index}`}>{recommendation}</li>
          ))}
        </ul>
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

      <button
        onClick={onReset}
        className="secondary-button"
        type="button"
      >
        Refazer análise
      </button>

      <p className="legal-note">
        Esta análise tem caráter informativo e não substitui orientação
        financeira profissional.
      </p>
    </section>
  );
}
