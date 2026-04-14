export default function ResultCard({ result, requestData, onReset }) {
  if (!result) return null;

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
        <h2>Seu diagnostico financeiro</h2>
      </div>

      <div className={`score-hero ${getTone(result.score)}`}>
        <span className="score-label">Score financeiro</span>
        <strong>{result.score.toFixed(2)}</strong>
      </div>

      <div className="result-meta">
        <span className={`badge ${getTone(result.score)}`}>
          {result.classificacao}
        </span>
      </div>

      <div className="result-copy">
        <h3>Recomendacao pratica</h3>
        <p>{result.recomendacao}</p>
      </div>

      {requestData ? (
        <div className="result-summary">
          <h3>Dados informados</h3>
          <dl>
            <div>
              <dt>Receita</dt>
              <dd>{requestData.receita}</dd>
            </div>
            <div>
              <dt>Despesas</dt>
              <dd>{requestData.despesas}</dd>
            </div>
            <div>
              <dt>Divida</dt>
              <dd>{requestData.divida}</dd>
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
        Esta analise tem carater informativo e nao substitui orientacao
        financeira profissional.
      </p>
    </section>
  );
}
