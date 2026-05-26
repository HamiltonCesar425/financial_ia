import { useState } from "react"
import { Routes, Route, useNavigate } from "react-router-dom"

import Home from "./features/essential-diagnosis/pages/Home"
import Privacy from "./features/essential-diagnosis/pages/Privacy"
import Feedback from "./features/essential-diagnosis/pages/Feedback"
import Contact from "./features/essential-diagnosis/pages/Contact"
import DataCollection from "./features/essential-diagnosis/pages/DataCollection"
import ResultPage from "./features/essential-diagnosis/pages/ResultPage"

import ScrollToTop from "./components/ScrollToTop"

import { generateDiagnosis } from "./services/api"

import { getHistory, saveAnalysis } from "./utils/historyStorage"

export default function App() {
  const navigate = useNavigate()

  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [lastPayload, setLastPayload] = useState(null)

  const history = getHistory()

  const insight = result?.insights || {
    message: "Análise indisponível.",
    trend: "stable",
    delta: 0,
  }

  const formattedDelta =
    insight?.delta === 0
      ? ""
      : `${insight?.delta > 0 ? "+" : ""}${insight?.delta} pts`

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

      navigate("/result")
    } catch (err) {
      if (err.response?.status === 422) {
        setError("Dados inválidos. Revise os campos informados.")
      } else if (err.response?.status === 500) {
        setError(
          "Não conseguimos concluir a análise agora. Tente novamente em instantes.",
        )
      } else if (err.code === "ECONNABORTED") {
        setError(
          "A análise demorou mais que o esperado. Verifique sua conexão e tente novamente.",
        )
      } else {
        setError(
          "Falha de conexão com o servidor. Verifique sua internet e tente novamente.",
        )
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <ScrollToTop />

      <Routes>
        <Route
          path="/"
          element={<Home onStart={() => navigate("/collection")} />}
        />

        <Route
          path="/collection"
          element={
            <DataCollection
              onSubmit={handleSubmit}
              loading={loading}
              error={error}
            />
          }
        />

        <Route
          path="/result"
          element={
            <ResultPage
              result={result}
              history={history}
              insight={insight}
              formattedDelta={formattedDelta}
              lastPayload={lastPayload}
              setResult={setResult}
              setLastPayload={setLastPayload}
            />
          }
        />

        <Route path="/privacy" element={<Privacy />} />

        <Route path="/feedback" element={<Feedback />} />

        <Route path="/contact" element={<Contact />} />
      </Routes>
    </>
  )
}
