import pandas as pd
import pytest

from src.engine.financial_metrics import (
    crescimento_medio,
    volatilidade,
    tendencia_linear,
    drawdown_max,
)

from src.engine.classification import classificar

from src.engine.pillar_scoring import (
    clamp,
    score_crescimento,
    score_estabilidade,
    score_consistencia,
    score_resiliencia,
)

from src.engine.calculation_engine import FinancialHealthEngine


# =========================
# FIXTURES
# =========================


@pytest.fixture
def sample_data():
    return [100, 110, 105, 120, 130]


# =========================
# FINANCIAL METRICS TESTS
# =========================


def test_crescimento_medio_crescente():
    serie = pd.Series([100, 110, 121])
    resultado = crescimento_medio(serie)
    assert round(resultado, 2) == 0.10


def test_crescimento_medio_constante():
    serie = pd.Series([100, 100, 100])
    resultado = crescimento_medio(serie)
    assert resultado == 0.0


def test_volatilidade_constante():
    serie = pd.Series([100, 100, 100])
    resultado = volatilidade(serie)
    assert resultado == 0.0


def test_volatilidade_variavel():
    serie = pd.Series([100, 120, 80, 130])
    resultado = volatilidade(serie)
    assert resultado > 0


def test_tendencia_linear_crescente():
    serie = pd.Series([100, 110, 120, 130])
    resultado = tendencia_linear(serie)
    assert resultado > 0


def test_tendencia_linear_decrescente():
    serie = pd.Series([130, 120, 110, 100])
    resultado = tendencia_linear(serie)
    assert resultado < 0


def test_tendencia_linear_constante():
    serie = pd.Series([100, 100, 100])
    resultado = tendencia_linear(serie)
    assert round(resultado, 5) == 0.0


def test_drawdown_max_com_queda():
    serie = pd.Series([100, 120, 90, 80])
    resultado = drawdown_max(serie)
    assert resultado < 0


def test_drawdown_sem_queda():
    serie = pd.Series([100, 110, 120])
    resultado = drawdown_max(serie)
    assert resultado == 0.0


def test_drawdown_extremo():
    serie = pd.Series([100, 50])
    resultado = drawdown_max(serie)
    assert resultado <= -0.5


# =========================
# CLASSIFICATION TESTS
# =========================


def test_classificacao_excelente():
    assert classificar(95) == "Excelente"


def test_classificacao_limite_excelente():
    assert classificar(90) == "Excelente"


def test_classificacao_bom():
    assert classificar(80) == "Bom"


def test_classificacao_limite_bom():
    assert classificar(75) == "Bom"


def test_classificacao_regular():
    assert classificar(60) == "Regular"


def test_classificacao_regular_limite():
    assert classificar(50) == "Regular"


def test_classificacao_critico():
    assert classificar(30) == "Crítico"


def test_classificacao_valor_negativo():
    assert classificar(-10) == "Crítico"


# =========================
# PILLAR SCORING TESTS
# =========================


def test_clamp_dentro_intervalo():
    assert clamp(50) == 50


def test_clamp_abaixo_minimo():
    assert clamp(-10) == 0


def test_clamp_acima_maximo():
    assert clamp(150) == 100


def test_score_crescimento_neutro():
    assert score_crescimento(0) == 50


def test_score_crescimento_alto():
    assert score_crescimento(1) == 100


def test_score_crescimento_negativo():
    assert score_crescimento(-0.2) < 50


def test_score_estabilidade_perfeita():
    assert score_estabilidade(0) == 100


def test_score_estabilidade_alta_volatilidade():
    assert score_estabilidade(1) == 0


def test_score_consistencia_neutra():
    assert score_consistencia(0) == 50


def test_score_consistencia_positiva():
    assert score_consistencia(0.2) > 50


def test_score_consistencia_negativa():
    assert score_consistencia(-0.2) < 50


def test_score_resiliencia_sem_perda():
    assert score_resiliencia(0) == 100


def test_score_resiliencia_com_perda():
    assert score_resiliencia(-0.5) < 100


def test_score_resiliencia_extremo():
    assert score_resiliencia(-2) == 0


# =========================
# ENGINE TESTS
# =========================


def test_engine_predict_valido(sample_data):
    engine = FinancialHealthEngine(window=4)
    resultado = engine.predict(sample_data)

    assert isinstance(resultado, dict)
    assert "score" in resultado
    assert "classification" in resultado
    assert "pillars" in resultado
    assert "metadata" in resultado


def test_engine_score_intervalo(sample_data):
    engine = FinancialHealthEngine(window=4)
    resultado = engine.predict(sample_data)

    assert 0 <= resultado["score"] <= 100


def test_engine_pillars_estrutura(sample_data):
    engine = FinancialHealthEngine(window=4)
    resultado = engine.predict(sample_data)

    pilares = resultado["pillars"]

    assert set(pilares.keys()) == {
        "crescimento",
        "estabilidade",
        "consistencia",
        "resiliencia",
    }

    for valor in pilares.values():
        assert 0 <= valor <= 100


def test_engine_metadata(sample_data):
    engine = FinancialHealthEngine(window=4)
    resultado = engine.predict(sample_data)

    metadata = resultado["metadata"]

    assert metadata["window"] == 4
    assert metadata["data_points"] == 4


def test_engine_input_tipo_invalido():
    engine = FinancialHealthEngine()

    with pytest.raises(TypeError):
        engine.predict("dados_invalidos")


def test_engine_dados_insuficientes():
    engine = FinancialHealthEngine(window=5)

    data = [100, 110, 120]

    with pytest.raises(ValueError):
        engine.predict(data)


def test_engine_compute_sem_coluna_receita():
    engine = FinancialHealthEngine(window=3)

    df = pd.DataFrame({"valor": [100, 110, 120]})

    with pytest.raises(ValueError):
        engine.compute(df)


def test_engine_compute_dados_insuficientes():
    engine = FinancialHealthEngine(window=5)

    df = pd.DataFrame({"receita": [100, 110, 120]})

    with pytest.raises(ValueError):
        engine.compute(df)


def test_engine_predict_com_none():
    engine = FinancialHealthEngine()

    with pytest.raises(Exception):
        engine.predict(None)
