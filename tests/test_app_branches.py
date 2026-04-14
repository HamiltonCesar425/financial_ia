import pytest
from src.api import app
from src.core import health_score

# -------------------------------
# 🟢 Testes de branches em app.py
# -------------------------------


def test_app_invalid_request(client):
    # Força um request inválido para cobrir branch de erro
    payload = {"receitas": 1000, "despesas": 500}
    response = client.post("/calcular", json=payload)
    assert response.status_code == 422


def test_app_missing_fields(client):
    # Request com campos faltando
    payload = {"dados": True, "receitas": 1000}
    response = client.post("/calcular", json=payload)
    assert response.status_code == 422  # Unprocessable Entity


# -------------------------------
# 🟡 Testes de branches em health_score.py
# -------------------------------


def test_health_score_negative_values():
    # Força valores negativos para ativar branch de erro
    dados = {"receitas": -1000, "despesas": 500}
    score = health_score.calcular(dados)
    assert isinstance(score, (int, float))


def test_health_score_high_volatility():
    # Força cenário de alta volatilidade para cobrir branch
    dados = {"receitas": 1000, "despesas": 950, "volatilidade": 0.9}
    score = health_score.calcular(dados)
    assert score <= 100  # score deve ser limitado


def test_health_score_empty_data():
    # Força branch de dados vazios
    with pytest.raises(ValueError):
        health_score.calcular({})
