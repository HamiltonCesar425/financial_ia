export function analyzeHistory(history) {
  if (!history || history.length < 2) {
    return {
      trend: "insufficient_data",
      volatility: "unknown",
      message: "Histórico insuficiente para análise evolutiva.",
    }
  }

  const scores = history.map((entry) => entry.score)

  const delta = scores[scores.length - 1] - scores[0]

  const volatility = calculateVolatility(scores)

  const trend = classifyTrend(delta)
  const volatilityLabel = classifyVolatility(volatility)

  return {
    trend,
    volatility: volatilityLabel,
    message: generateMessage(trend, volatilityLabel),
  }
}

function classifyTrend(delta) {
  if (delta > 20) return "improving"
  if (delta < -20) return "declining"
  return "stable"
}

function classifyVolatility(volatility) {
  if (volatility > 40) return "high"
  if (volatility > 20) return "moderate"
  return "low"
}

function calculateVolatility(scores) {
  const mean = scores.reduce((sum, value) => sum + value, 0) / scores.length

  const variance = scores.reduce((sum, value) => sum + Math.pow(value - mean, 2), 0) / scores.length

  return Math.sqrt(variance)
}

function generateMessage(trend, volatility) {
  if (trend === "improving" && volatility === "low") {
    return "Seu histórico demonstra evolução consistente e estabilidade crescente."
  }

  if (trend === "declining") {
    return "Foi detectada deterioração progressiva no score financeiro."
  }

  if (volatility === "high") {
    return "Seu histórico apresenta oscilações relevantes."
  }

  return "Seu histórico permanece relativamente estável."
}
