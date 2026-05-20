from typing import Dict

from src.app.schemas.prediction import PredictionResponse


CONFIDENCE_FORMULA = (
    "Confiança = 1 - variância dos sinais normalizados "
    "(liquidez, dívida, estabilidade e fluxo de caixa)."
)


def build_projection_explanation(historical_delta: float, projected_delta: float) -> str:
    if historical_delta < 0 and projected_delta > 0:
        return (
            "Apesar da queda recente no histórico, a projeção considera os indicadores "
            "atuais de estabilidade e fluxo de caixa, que sinalizam recuperação nos próximos 30 dias."
        )

    if historical_delta > 0 and projected_delta < 0:
        return (
            "Mesmo com melhora recente no histórico, os indicadores atuais sugerem pressão "
            "sobre o score nos próximos 30 dias."
        )

    if abs(projected_delta) <= 5:
        return (
            "A projeção indica estabilidade porque os sinais atuais não apontam "
            "pressão relevante de melhora ou deterioração."
        )

    return "Projeção baseada na estabilidade atual do fluxo financeiro."


class PredictionEngine:
    """
    Engine responsible for forecasting future financial scores
    based on current financial metrics.
    """

    LIQUIDITY_WEIGHT = 0.35
    DEBT_WEIGHT = 0.30
    STABILITY_WEIGHT = 0.20
    CASHFLOW_WEIGHT = 0.15

    def predict_score_30d(
        self, current_score: int, metrics: Dict
    ) -> PredictionResponse:

        liquidity = self._calculate_liquidity_momentum(metrics)
        debt = self._calculate_debt_pressure(metrics)
        stability = self._calculate_financial_stability(metrics)
        cashflow = self._calculate_cashflow_trend(metrics)

        signals = {
            "liquidity": liquidity,
            "debt": debt,
            "stability": stability,
            "cashflow": cashflow,
        }

        delta = int(
            (
                liquidity * self.LIQUIDITY_WEIGHT
                - debt * self.DEBT_WEIGHT
                + stability * self.STABILITY_WEIGHT
                + cashflow * self.CASHFLOW_WEIGHT
            )
            * 100
        )

        projected_score = max(0, min(current_score + delta, 100))

        if delta > 25:
            trend = "positive"
        elif delta < -25:
            trend = "negative"
        else:
            trend = "stable"

        confidence = self._calculate_confidence(signals)

        factors = []

        if liquidity > 0.7:
            factors.append("Perspectiva de liquidez favorável")

        if debt > 0.7:
            factors.append("Pressão elevada de endividamento")

        if stability > 0.7:
            factors.append("Estrutura financeira estável")

        if cashflow > 0.7:
            factors.append("Tendência positiva de fluxo de caixa")

        return PredictionResponse(
            current_score=current_score,
            projected_score_30d=projected_score,
            delta=delta,
            trend=trend,
            confidence=confidence,
            confidence_formula=CONFIDENCE_FORMULA,
            confidence_factors=signals,
            projection_horizon_days=30,
            prediction_context=build_projection_explanation(0, delta),
            explanatory_factors=factors,
        )

    def _calculate_liquidity_momentum(self, metrics: Dict) -> float:
        return min(metrics.get("liquidity_ratio", 0), 1.0)

    def _calculate_debt_pressure(self, metrics: Dict) -> float:
        return min(metrics.get("debt_ratio", 0), 1.0)

    def _calculate_financial_stability(self, metrics: Dict) -> float:
        return min(metrics.get("stability_score", 0), 1.0)

    def _calculate_cashflow_trend(self, metrics: Dict) -> float:
        return min(metrics.get("cashflow_trend", 0), 1.0)

    def _calculate_confidence(self, signals: Dict) -> float:
        values = list(signals.values())

        mean = sum(values) / len(values)

        variance = sum((value - mean) ** 2 for value in values) / len(values)

        confidence = 1 - variance

        return round(max(0.0, min(confidence, 1.0)), 2)
