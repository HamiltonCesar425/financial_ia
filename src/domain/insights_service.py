def generate_insights(score: int) -> dict:
    if score < 50:
        return {
            "message": "Alto risco financeiro",
            "recommendation": "Reduzir despesas fixas"
        }
    return {
        "message": "Situação estável",
        "recommendation": "Otimizar investimentos"
    }