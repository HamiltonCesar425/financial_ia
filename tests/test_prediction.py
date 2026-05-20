from src.app.schemas.prediction import PredictionResponse
from src.app.services.prediction_engine import (
    CONFIDENCE_FORMULA,
    PredictionEngine,
    build_projection_explanation,
)


def test_predict_score_30d_returns_expected_projection():
    engine = PredictionEngine()

    result = engine.predict_score_30d(
        current_score=720,
        metrics={
            "liquidity_ratio": 0.82,
            "debt_ratio": 0.35,
            "stability_score": 0.78,
            "cashflow_trend": 0.74,
        },
    )

    assert isinstance(result, PredictionResponse)
    assert result.current_score == 720
    assert result.delta == 44
    assert result.projected_score_30d == 100
    assert result.trend == "positive"
    assert result.confidence == 0.96
    assert result.confidence_formula == CONFIDENCE_FORMULA
    assert result.confidence_factors == {
        "liquidity": 0.82,
        "debt": 0.35,
        "stability": 0.78,
        "cashflow": 0.74,
    }
    assert result.projection_horizon_days == 30
    assert (
        result.prediction_context
        == "Projeção baseada na estabilidade atual do fluxo financeiro."
    )
    assert result.explanatory_factors == [
        "Perspectiva de liquidez favorável",
        "Estrutura financeira estável",
        "Tendência positiva de fluxo de caixa",
    ]


def test_predict_score_30d_caps_projected_score_at_100():
    engine = PredictionEngine()

    result = engine.predict_score_30d(
        current_score=990,
        metrics={
            "liquidity_ratio": 1.0,
            "debt_ratio": 0.0,
            "stability_score": 1.0,
            "cashflow_trend": 1.0,
        },
    )

    assert result.projected_score_30d == 100
    assert result.delta == 70
    assert result.trend == "positive"


def test_predict_score_30d_caps_projected_score_at_zero():
    engine = PredictionEngine()

    result = engine.predict_score_30d(
        current_score=10,
        metrics={
            "liquidity_ratio": 0.0,
            "debt_ratio": 1.0,
            "stability_score": 0.0,
            "cashflow_trend": 0.0,
        },
    )

    assert result.projected_score_30d == 0
    assert result.delta == -30
    assert result.trend == "negative"
    assert result.explanatory_factors == ["Pressão elevada de endividamento"]


def test_predict_score_30d_defaults_missing_metrics_to_stable_projection():
    engine = PredictionEngine()

    result = engine.predict_score_30d(current_score=50, metrics={})

    assert result.projected_score_30d == 50
    assert result.delta == 0
    assert result.trend == "stable"
    assert result.confidence == 1.0
    assert result.prediction_context == (
        "A projeção indica estabilidade porque os sinais atuais não apontam "
        "pressão relevante de melhora ou deterioração."
    )
    assert result.explanatory_factors == []


def test_projection_context_explains_recovery_after_historical_drop():
    prediction = PredictionEngine().predict_score_30d(
        current_score=78,
        metrics={
            "liquidity_ratio": 0.8,
            "debt_ratio": 0.2,
            "stability_score": 0.82,
            "cashflow_trend": 0.78,
        },
    )
    context = build_projection_explanation(
        historical_delta=-10,
        projected_delta=prediction.delta,
    )

    assert prediction.delta > 0
    assert context == (
        "Apesar da queda recente no histórico, a projeção considera os indicadores "
        "atuais de estabilidade e fluxo de caixa, que sinalizam recuperação nos próximos 30 dias."
    )


def test_projection_context_explains_retraction_after_historical_improvement():
    prediction = PredictionEngine().predict_score_30d(
        current_score=70,
        metrics={
            "liquidity_ratio": 0.0,
            "debt_ratio": 1.0,
            "stability_score": 0.0,
            "cashflow_trend": 0.0,
        },
    )
    context = build_projection_explanation(
        historical_delta=12,
        projected_delta=prediction.delta,
    )

    assert prediction.delta < 0
    assert context == (
        "Mesmo com melhora recente no histórico, os indicadores atuais sugerem pressão "
        "sobre o score nos próximos 30 dias."
    )


def test_projection_context_explains_neutral_stability():
    prediction = PredictionEngine().predict_score_30d(
        current_score=50,
        metrics={
            "liquidity_ratio": 0.0,
            "debt_ratio": 0.0,
            "stability_score": 0.0,
            "cashflow_trend": 0.0,
        },
    )
    context = build_projection_explanation(
        historical_delta=0,
        projected_delta=prediction.delta,
    )

    assert prediction.delta == 0
    assert context == (
        "A projeção indica estabilidade porque os sinais atuais não apontam "
        "pressão relevante de melhora ou deterioração."
    )
