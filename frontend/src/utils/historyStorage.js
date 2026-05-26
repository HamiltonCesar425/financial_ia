const STORAGE_KEY = "financial_ia_history"

export function getHistory() {
  try {
    const data = localStorage.getItem(STORAGE_KEY)
    const parsedData = data ? JSON.parse(data) : []

    return Array.isArray(parsedData) ? parsedData : []
  } catch {
    localStorage.removeItem(STORAGE_KEY)
    return []
  }
}

export function saveAnalysis(result, requestData) {
  const history = getHistory()
  const score = result?.score ?? result?.financial_score ?? 0

  const newEntry = {
    id: crypto.randomUUID(),
    timestamp: new Date().toISOString(),
    score,
    classification: result?.classification || "Indefinido",
    receita: requestData.receita,
    despesas: requestData.despesas,
    divida: requestData.divida,
    reserva: requestData.reserva,
  }

  const updatedHistory = [...history, newEntry].slice(-20)

  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(updatedHistory))
  } catch {
    // Storage can fail in private mode or when quota is exceeded.
  }
}

export function clearHistory() {
  localStorage.removeItem(STORAGE_KEY)
}
