import pandas as pd
import numpy as np
import pytest

from src.core.health_score import calcular_indice_saude


def df(valores):
    return pd.DataFrame({"receita": valores})


# =========================
# TESTES PARAMETRIZADOS (CORE)
# =========================
@pytest.mark.parametrize(
    "valores, rmse",
    [
        ([100, 200, 50, 30], 100),
        ([100, 300, 50, 400, 30], 10),
        ([500, 400, 300, 200], 50),
        ([100, 200, 300, 400], 50),
        ([100, 110, 120, 130], 1),
        ([100, 110, 120, 130], 10000),
        ([100, -200, 300, -400, 500], 500),
        ([100, None, 120, 130], 10),
        ([1e6, 2e6, 3e6, 4e6], 1000),
    ],
)
def test_calcular_indice_saude_multiplos(valores, rmse):
    data = df(valores).fillna(0)
    result = calcular_indice_saude(data, rmse=rmse)

    assert isinstance(result, dict)
    assert "indice" in result
    assert 0 <= result["indice"] <= 100


# =========================
# EDGE CASES - SERIES (branches críticos)
# =========================
def test_series_tamanho_um():
    data = df([1000])
    result = calcular_indice_saude(data)
    assert 0 <= result["indice"] <= 100


def test_series_com_zeros():
    data = df([0, 0, 0])
    result = calcular_indice_saude(data)
    assert 0 <= result["indice"] <= 100


def test_series_com_divisao_protegida():
    data = df([0, 100, 200])
    result = calcular_indice_saude(data)
    assert 0 <= result["indice"] <= 100


def test_series_curta_momentum():
    data = df([100, 200])
    result = calcular_indice_saude(data)
    assert 0 <= result["indice"] <= 100


# =========================
# RMSE BRANCHES
# =========================
def test_rmse_none():
    data = df([100, 200, 300])
    result = calcular_indice_saude(data, rmse=None)
    assert 0 <= result["indice"] <= 100


def test_rmse_valido():
    data = df([100, 200, 300])
    result = calcular_indice_saude(data, rmse=50)
    assert 0 <= result["indice"] <= 100


def test_rmse_invalido_tipo():
    data = df([100, 200, 300])
    with pytest.raises(ValueError):
        calcular_indice_saude(data, rmse="erro")


def test_rmse_negativo():
    data = df([100, 200, 300])
    with pytest.raises(ValueError):
        calcular_indice_saude(data, rmse=-1)


# =========================
# PRESET E PESOS
# =========================
def test_preset_invalido():
    data = df([100, 200, 300])
    with pytest.raises(ValueError):
        calcular_indice_saude(data, preset="inexistente")


def test_pesos_invalidos_soma():
    data = df([100, 200, 300])
    pesos = {
        "crescimento": 0.5,
        "volatilidade": 0.5,
        "momentum": 0.5,
        "erro_modelo": -0.5,
    }
    with pytest.raises(ValueError):
        calcular_indice_saude(data, pesos=pesos)


# =========================
# VALIDAÇÕES DE DATAFRAME
# =========================
def test_dataframe_vazio():
    data = df([])
    with pytest.raises(ValueError):
        calcular_indice_saude(data)


def test_tipo_invalido():
    with pytest.raises(ValueError):
        calcular_indice_saude("entrada_invalida")


def test_sem_coluna_receita():
    data = pd.DataFrame({"x": [1, 2]})
    with pytest.raises(ValueError):
        calcular_indice_saude(data)