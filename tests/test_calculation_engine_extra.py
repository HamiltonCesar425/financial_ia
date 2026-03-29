import pytest
import pandas as pd
from src.engine.calculation_engine import FinancialHealthEngine


# ==============================
# Testes de cenários válidos
# ==============================
def test_predict_valido():
    engine = FinancialHealthEngine(window=12)
    data = [1000] * 12
    resultado = engine.predict(data)
    assert isinstance(resultado, dict)
    assert "score" in resultado
    assert "classification" in resultado


# ==============================
# Testes de cenários de erro em predict
# ==============================
def test_predict_tipo_invalido():
    engine = FinancialHealthEngine(window=12)
    with pytest.raises(TypeError, match="Entrada deve ser uma lista"):
        engine.predict("não é lista")


def test_predict_dados_insuficientes():
    engine = FinancialHealthEngine(window=12)
    with pytest.raises(
        ValueError, match="São necessários pelo menos 12 pontos de dados"
    ):
        engine.predict([1000] * 5)


def test_predict_dataframe_invalido(monkeypatch):
    engine = FinancialHealthEngine(window=12)

    # força erro na criação do DataFrame
    monkeypatch.setattr(
        "pandas.DataFrame",
        lambda *args, **kwargs: (_ for _ in ()).throw(Exception("Erro simulado")),
    )

    with pytest.raises(ValueError, match="Erro ao converter dados para DataFrame"):
        engine.predict([1000] * 12)


# ==============================
# Testes de cenários de erro em compute
# ==============================
def test_compute_sem_coluna_receita():
    engine = FinancialHealthEngine(window=12)
    df = pd.DataFrame({"outra_coluna": [1000] * 12})
    with pytest.raises(ValueError, match="DataFrame deve conter coluna 'receita'"):
        engine.compute(df)


def test_compute_dados_insuficientes():
    engine = FinancialHealthEngine(window=12)
    df = pd.DataFrame({"receita": [1000] * 5})
    with pytest.raises(ValueError, match="Dados insuficientes para cálculo"):
        engine.compute(df)
