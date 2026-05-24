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
    return <p>Nenhum resultado disponível.</p>
  }

  const prediction = result?.prediction

  const predictionFactors =
    prediction?.explanatory_factors?.filter(Boolean) || []

  const chartData =
    history?.map((item, index) => ({
      index: index + 1,
      score: item?.result?.financial_score || 0,
    })) || []

  const handleReset = () => {
    setResult(null)
    setLastPayload(null)

    navigate("/collection")
  }

  return (
    <div className="w-full">
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

              <strong>{prediction.projected_score_30d}</strong>
            </div>

            <div>
              <span>Tendência</span>

              <strong>
                {predictionTrendLabels[prediction.trend] || "Estável"}
              </strong>
            </div>

            <div>
              <span>Confiança</span>

              <strong>{Math.round(prediction.confidence * 100)}%</strong>
            </div>

            <div>
              <span>Variação projetada</span>

              <strong>
                {prediction.delta > 0 ? "+" : ""}
                {prediction.delta.toFixed(1)}
              </strong>
            </div>
          </div>

          <p>{prediction.prediction_context}</p>

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
    </div>
  )
}
