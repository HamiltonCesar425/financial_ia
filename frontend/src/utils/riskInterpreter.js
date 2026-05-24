export function interpretRisk(score) {
  if (score >= 80) {
    return "baixo"
  }

  if (score >= 50) {
    return "moderado"
  }

  return "alto"
}
