from typing import Dict, Mapping

from src.domain.insights_service import generate_insights


def generate_diagnosis(data: Mapping[str, float]) -> Dict[str, object]:
    """
    Gera um diagnóstico financeiro puro e determinístico.
    """
    receita = float(data["receita"])
    despesas = float(data["despesas"])

    if receita <= 0:
        raise ValueError("Receita deve ser maior que zero")

    if despesas < 0:
        raise ValueError("Despesas não podem ser negativas")

    ratio = despesas / receita
    score = max(0, min(100, int(round(100 - (ratio * 100)))))
    insights = generate_insights(score)

    return {
        "score": score,
        "message": insights["message"],
        "recommendation": insights["recommendation"],
    }
