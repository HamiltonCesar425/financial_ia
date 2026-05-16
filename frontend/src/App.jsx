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
    return (
      <div className="w-full">
        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 mb-8">
          <h3 className="text-ig font-semibold text-slate-800 mb-2">
            Análise Evolutiva
          </h3>
          <p className="text-slate-600 leading-relaxed">
            {insight.message}
          </p>
        </div>
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
