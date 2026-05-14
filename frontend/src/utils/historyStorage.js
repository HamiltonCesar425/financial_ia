const STORAGE_KEY = "financial_ia_history";

export function getHistory() {
  const data = localStorage.getItem(STORAGE_KEY);
  return data ? JSON.parse(data) : [];
}

export function saveAnalysis(result, requestData) {
  const history = getHistory();

  const newEntry = {
    id: crypto.randomUUID(),
    timestamp: new Date().toISOString(),
    score: result.score,
    classification: result.classification,
    receita: requestData.receita,
    despesas: requestData.despesas,
    divida: requestData.divida,
    reserva: requestData.reserva,
  };

  const updatedHistory = [...history, newEntry].slice(-20);

  localStorage.setItem(STORAGE_KEY, JSON.stringify(updatedHistory));
}

export function clearHistory() {
  localStorage.removeItem(STORAGE_KEY);
}