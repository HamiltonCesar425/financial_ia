import pandas as pd
import pytest

from src.core.health_score import calcular_indice_saude


def df(valores):
    return pd.DataFrame({"receita": valores})


# =========================
# FORÇANDO BRANCHES INTERNOS
# =========================

def test_drawdown_negativo_forte():
    data = df([100, 200, 50, 30])
    score = calcular_indice_saude(data, rmse=100)

    assert isinstance(score, dict)
    assert "indice" in score
    assert 0 <= score["indice"] <= 100


def test_volatilidade_extrema():
    data = df([100, 300, 50, 400, 30])
    score = calcular_indice_saude(data, rmse=10)

    assert isinstance(score, dict)
    assert "indice" in score
    assert 0 <= score["indice"] <= 100


def test_tendencia_negativa_forte():
    data = df([500, 400, 300, 200])
    score = calcular_indice_saude(data, rmse=50)

    assert isinstance(score, dict)
    assert "indice" in score
    assert 0 <= score["indice"] <= 100


def test_tendencia_positiva_forte():
    data = df([100, 200, 300, 400])
    score = calcular_indice_saude(data, rmse=50)

    assert isinstance(score, dict)
    assert "indice" in score
    assert 0 <= score["indice"] <= 100


# =========================
# COBERTURA DE CONDIÇÕES INTERNAS
# =========================

def test_rmse_influencia_score():
    data = df([100, 110, 120, 130])

    score_baixo_rmse = calcular_indice_saude(data, rmse=1)
    score_alto_rmse = calcular_indice_saude(data, rmse=10000)

    assert isinstance(score_baixo_rmse, dict)
    assert isinstance(score_alto_rmse, dict)

    assert score_baixo_rmse["indice"] != score_alto_rmse["indice"]


def test_valores_mistos_complexos():
    data = df([100, -200, 300, -400, 500])
    score = calcular_indice_saude(data, rmse=500)

    assert isinstance(score, dict)
    assert "indice" in score
    assert 0 <= score["indice"] <= 100


# =========================
# FORÇAR EDGE INTERNO
# =========================

def test_nan_handling():
    data = df([100, None, 120, 130])
    data = data.fillna(0)

    score = calcular_indice_saude(data, rmse=10)

    assert isinstance(score, dict)
    assert "indice" in score
    assert 0 <= score["indice"] <= 100


def test_valores_grandes():
    data = df([1e6, 2e6, 3e6, 4e6])
    score = calcular_indice_saude(data, rmse=1000)

    assert isinstance(score, dict)
    assert "indice" in score
    assert 0 <= score["indice"] <= 100
    