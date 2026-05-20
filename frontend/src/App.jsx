import { useState } from "react"

import ResultCard from "./components/ResultCard"
import { generateDiagnosis } from "./services/api"

import HistoryPanel from "./components/HistoryPanel"
import ScoreHistoryChart from "./features/essential-diagnosis/components/ScoreHistoryChart"
import DataCollection from "./features/essential-diagnosis/pages/DataCollection"
import Landing from "./features/essential-diagnosis/pages/Landing"
import { getHistory, saveAnalysis } from "./utils/historyStorage"

export default function App() {
  const [step, setStep] = useState("landing")
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [lastPayload, setLastPayload] = useState(null)

  const history = getHistory()

  const insight = result?.insights || {
    message: "Análise indisponível.",
  }

  const chartData = getHistory().map((entry) => ({
    date: new Date(entry.timestamp).toLocaleDateString("pt-BR", {
      day: "2-digit",
      month: "2-digit",
    }),
    score: entry.score,
  }))

  const trendLabels = {
    ASCENDENTE: "Ascendente",
    ESTAVEL: "Estável",
    DESCENDENTE: "Descendente",
    CRITICA: "Crítica",
  }

  const formattedDelta =
    insight?.delta === 0 ? "" : `${insight?.delta > 0 ? "+" : ""}${insight?.delta} pts`

  const handleSubmit = async (data) => {
    setLoading(true)
    setError(null)

    try {
      const response = await generateDiagnosis({
        ...data,
        history,
      })

      setResult(response)
      setLastPayload(data)
      saveAnalysis(response, data)
      setStep("result")
    } catch (err) {
      if (err.response?.status === 422) {
        setError("Dados inválidos. Revise os campos informados.")
      } else if (err.response?.status === 500) {
        setError("Erro interno do servidor.")
      } else {
        setError("Falha de conexão com o servidor.")
      }
    } finally {
      setLoading(false)
    }
  }

  if (step === "landing") {
    return <Landing onStart={() => setStep("collection")} />
  }

  if (step === "collection") {
    return <DataCollection onSubmit={handleSubmit} loading={loading} error={error} />
  }

  if (step === "result") {
    const prediction = result?.prediction
    const predictionFactors = prediction?.explanatory_factors?.filter(Boolean) || []
    const predictionTrendLabels = {
      positive: "Positiva",
      stable: "Estável",
      negative: "Negativa",
    }

    return (
      <div className="w-full">
        <div className="insight-card">
          <h3>Análise Evolutiva</h3>

          <p>{insight.message}</p>

          <div className="insight-meta">
            <span>{trendLabels[insight.trend]}</span>
            {formattedDelta && <span>• Variação histórica: {formattedDelta}</span>}
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
                <strong>{predictionTrendLabels[prediction.trend] || "Estável"}</strong>
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

            <p>
              {prediction.prediction_context}
            </p>

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
          onReset={() => {
            setResult(null)
            setLastPayload(null)
            setStep("collection")
          }}
        />

        <ScoreHistoryChart data={chartData} />

        <HistoryPanel />
      </div>
    )
  }

  return null
}
