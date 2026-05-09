import { useState } from "react";
import ResultCard from "./components/ResultCard";
import { calculateScore } from "./services/api";
import Landing from "./features/essential-diagnosis/pages/Landing";
import DataCollection from "./features/essential-diagnosis/pages/DataCollection";

export default function App() {
  const [step, setStep] = useState("landing");
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
      setStep("result");
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

  if (step === "landing") {
    return <Landing onStart={() => setStep("collection")} />;
  }

  if (step === "collection") {
    return (
      <DataCollection
        onSubmit={handleSubmit}
        loading={loading}
        error={error}
      />
    );
  }

  if (step === "result") {
    return (
      <ResultCard
        result={result}
        payload={lastPayload}
      />
    );
  }

  return null;
}
