from src.domain.insights_service import generate_insights


def test_generate_insights_high_risk():
    result = generate_insights(40)

    assert result["message"] == "Alto risco financeiro"
    assert result["recommendation"] == "Reduzir despesas fixas"


def test_generate_insights_stable():
    result = generate_insights(80)

    assert result["message"] == "Situação estável"
    assert result["recommendation"] == "Otimizar investimentos"