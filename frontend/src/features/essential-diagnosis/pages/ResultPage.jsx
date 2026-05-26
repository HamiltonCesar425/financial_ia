import { useNavigate } from "react-router-dom"

import HistoryPanel from "../../../components/HistoryPanel"
import ResultCard from "../../../components/ResultCard"

import ScoreHistoryChart from "../components/ScoreHistoryChart"

const predictionTrendLabels = {
  improving: "Melhora",
  stable: "Estável",
  declining: "Declínio",
}

export default function ResultPage({
  result,
  history,
  insight,
  formattedDelta,
  lastPayload,
  setResult,
  setLastPayload,
}) {
  const navigate = useNavigate()

  if (!result) {
    return (
      <main className="empty-state-page">
        <section className="card empty-state-card">
          <span className="eyebrow">Resultado</span>
          <h1>Nenhum diagnóstico disponível</h1>
          <p>
            Inicie uma nova análise para gerar seu score financeiro e visualizar
            recomendações personalizadas.
          </p>
          <button
            className="primary-button"
            type="button"
            onClick={() => navigate("/collection")}
          >
            Iniciar análise
          </button>
        </section>
      </main>
    )
  }

  const prediction = result?.prediction

  const predictionFactors =
    prediction?.explanatory_factors?.filter(Boolean) || []

  const chartData =
    history?.map((item, index) => ({
      label: item?.timestamp
        ? new Date(item.timestamp).toLocaleDateString("pt-BR")
        : `Análise ${index + 1}`,
      score:
        item?.score ??
        item?.result?.score ??
        item?.result?.financial_score ??
        0,
    })) || []

  const handleReset = () => {
    setResult(null)
    setLastPayload(null)

    navigate("/collection")
  }

  return (
    <main className="result-page">
      <div className="insight-card">
        <h3>Análise Evolutiva</h3>

        <p>{insight.message}</p>

        <div className="insight-meta">
          <span>{predictionTrendLabels[insight.trend] || "Estável"}</span>

          {formattedDelta && (
            <span>• Variação histórica: {formattedDelta}</span>
          )}
        </div>
      </div>

      {prediction && (
        <div className="insight-card prediction-card">
          <h3>Projeção Financeira (30 dias)</h3>

          <div className="prediction-summary">
            <div>
              <span>Score projetado</span>

              <strong>{prediction.projected_score_30d ?? "-"}</strong>
            </div>

            <div>
              <span>Tendência</span>

              <strong>
                {predictionTrendLabels[prediction.trend] || "Estável"}
              </strong>
            </div>

            <div>
              <span>Confiança</span>

              <strong>
                {Number.isFinite(prediction.confidence)
                  ? `${Math.round(prediction.confidence * 100)}%`
                  : "-"}
              </strong>
            </div>

            <div>
              <span>Variação projetada</span>

              <strong>
                {Number.isFinite(prediction.delta)
                  ? `${prediction.delta > 0 ? "+" : ""}${prediction.delta.toFixed(1)}`
                  : "-"}
              </strong>
            </div>
          </div>

          {prediction.prediction_context ? (
            <p className="prediction-context">
              {prediction.prediction_context}
            </p>
          ) : null}

          {predictionFactors.length > 0 ? (
            <ul className="prediction-factors">
              {predictionFactors.map((factor, index) => (
                <li key={`${factor}-${index}`}>{factor}</li>
              ))}
            </ul>
          ) : (
            <p className="prediction-empty">
              Nenhum fator crítico adicional foi identificado nesta projeção.
            </p>
          )}
        </div>
      )}

      <ResultCard
        result={result}
        requestData={lastPayload}
        onReset={handleReset}
      />

      <ScoreHistoryChart data={chartData} />

      <HistoryPanel />
    </main>
  )
}
