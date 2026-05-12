import { useState } from "react";

import ResultCard from "./components/ResultCard";
import { generateDiagnosis } from "./services/api";

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
      const response = await generateDiagnosis(data);

      setResult(response);
      setLastPayload(data);
      setStep("result");
    } catch (err) {
      if (err.response?.status === 422) {
        setError("Dados inválidos. Revise os campos informados.");
      } else if (err.response?.status === 500) {
        setError("Erro interno do servidor.");
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
        requestData={lastPayload}
        onReset={() => {
          setResult(null);
          setLastPayload(null);
          setStep("collection");
        }}
      />
    );
  }

  return null;
}
