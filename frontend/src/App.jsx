import { useState } from "react";
import HeroSection from "./components/HeroSection";
import ValueHighlights from "./components/ValueHighlights";
import ScoreForm from "./components/ScoreForm";
import ResultCard from "./components/ResultCard";
import ErrorNotice from "./components/ErrorNotice";
import { calculateScore } from "./services/api";

export default function App() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [lastPayload, setLastPayload] = useState(null);

  const handleSubmit = async (data) => {
    setLoading(true);
    setError(null);

    try {
      const response = await calculateScore(data);
      setResult(response.data);
      setLastPayload(data);

      setTimeout(() => {
        document.getElementById("result")?.scrollIntoView({
          behavior: "smooth",
        });
      }, 100);
    } catch (err) {
      if (err.response?.status === 422) {
        setError("Dados inválidos. Verifique os campos.");
      } else if (err.response?.status === 500) {
        setError("Erro interno. Tente novamente.");
      } else {
        setError("Falha de conexão com o servidor.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-shell">
      <main className="page-content">
        <HeroSection />
        <ValueHighlights />
        <section className="card panel-section">
          <div className="section-heading">
            <span className="eyebrow">Analise agora</span>
            <h2>Receba seu diagnostico financeiro</h2>
            <p>
              Preencha os campos abaixo para calcular seu score, entender sua
              classificacao e receber uma recomendacao pratica.
            </p>
          </div>
          <ErrorNotice message={error} />
          <ScoreForm onSubmit={handleSubmit} loading={loading} />
        </section>
        <div id="result">
          <ResultCard
            result={result}
            requestData={lastPayload}
            onReset={() => {
              setResult(null);
              setLastPayload(null);
              setError(null);
            }}
          />
        </div>
      </main>
      <footer className="footer-note">
        Diagnostico Financeiro Automatizado. Esta analise tem carater
        informativo e nao substitui orientacao financeira profissional.
      </footer>
    </div>
  );
}
