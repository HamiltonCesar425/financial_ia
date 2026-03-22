def test_engine_prediction():
    from src.engine.calculation_engine import FinancialHealthEngine

    engine = FinancialHealthEngine()

    data = [1000] * 12
    result = engine.predict(data)

    assert result is not None
    