from typing import Dict, Mapping
from src.app.services.prediction_engine import PredictionEngine



def _classify(score: int) -> str:
    if score < 30:
        return "Crítico"
    if score < 50:
        return "Atenção"
    if score < 75:
        return "Estável"
    return "Saudável"


def _generate_alerts(
    receita: float,
    despesas: float,
    divida: float,
    reserva: float,
) -> list[str]:
    alerts = []

    if despesas / receita > 0.7:
        alerts.append("Comprometimento elevado da renda")

    if divida > receita * 0.5:
        alerts.append("Nível de endividamento acima do ideal")

    if reserva < despesas * 3:
        alerts.append("Reserva financeira abaixo da cobertura recomendada")

    while len(alerts) < 3:
        alerts.append("Necessidade de monitoramento preventivo")

    return alerts[:3]


def _generate_recommendations(
    receita: float,
    despesas: float,
    divida: float,
    reserva: float,
) -> list[str]:
    recommendations = []

    if despesas / receita > 0.7:
        recommendations.append("Reduzir despesas variáveis em pelo menos 10%")

    if divida > receita * 0.5:
        recommendations.append("Priorizar amortização progressiva das dívidas")

    if reserva < despesas * 3:
        recommendations.append("Construir reserva equivalente a 3 meses de despesas")

    while len(recommendations) < 3:
        recommendations.append("Realizar revisão financeira mensal")

    return recommendations[:3]


def generate_diagnosis(data: Mapping[str, float]) -> Dict[str, object]:
    receita = float(data["receita"])
    despesas = float(data["despesas"])
    divida = float(data["divida"])
    reserva = float(data["reserva"])

    if receita <= 0:
        raise ValueError("Receita deve ser maior que zero")

    if despesas < 0:
        raise ValueError("Despesas não podem ser negativas")

    if divida < 0:
        raise ValueError("Dívida não pode ser negativa")

    if reserva < 0:
        raise ValueError("Reserva não pode ser negativa")

    ratio = despesas / receita
    debt_weight = divida / receita
    reserve_bonus = min(reserva / despesas, 3) * 5 if despesas > 0 else 15

    raw_score = 100 - (ratio * 60) - (debt_weight * 25) + reserve_bonus
    score = max(0, min(100, int(round(raw_score))))

    classification = _classify(score)

    prediction_engine = PredictionEngine()

    prediction = prediction_engine.predict_score_30d(
        current_score=score,
        metrics={
            "liquidity_ratio": min(reserva / receita, 1.0),
            "debt_ratio": min(divida / receita, 1.0),
            "stability_score": max(0.0, 1 - ratio),
            "cashflow_trend": max(0.0, min((receita - despesas) / receita, 1.0)),
        }
    )

    diagnosis_map = {
        "Crítico": (
            "Sua saúde financeira apresenta vulnerabilidade severa "
            "e requer correções imediatas."
        ),
        "Atenção": (
            "Seu cenário financeiro exige ajustes relevantes "
            "para evitar deterioração."
        ),
        "Estável": (
            "Sua saúde financeira demonstra estabilidade moderada, "
            "com pontos importantes de melhoria."
        ),
        "Saudável": (
            "Seu cenário financeiro demonstra boa solidez "
            "e capacidade de sustentação."
        ),
    }

    return {
        "score": score,
        "classification": classification,
        "diagnosis": diagnosis_map[classification],
        "alerts": _generate_alerts(
            receita,
            despesas,
            divida,
            reserva,
        ),
        "recommendations": _generate_recommendations(
            receita,
            despesas,
            divida,
            reserva,
        ),
        "prediction": prediction.model_dump(),
    }
