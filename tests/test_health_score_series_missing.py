import numpy as np
import pytest
from src.core.health_score import calcular_indice_saude_series


# 1. Série com 1 elemento (branch growth)
def test_series_tamanho_um():
    receita = np.array([1000])
    result = calcular_indice_saude_series(receita)
    assert "indice" in result


# 2. Valores zero (branch vi <= 0)
def test_series_valores_zero():
    receita = np.array([0, 0, 0])
    result = calcular_indice_saude_series(receita)
    assert result["indice"] >= 0


# 3. Denominator zero (proteção divisão)
def test_series_com_zero_no_denominador():
    receita = np.array([0, 100, 200])
    result = calcular_indice_saude_series(receita)
    assert result["indice"] >= 0


# 4. Série curta (<3 → momentum)
def test_series_curta_momentum():
    receita = np.array([100, 200])
    result = calcular_indice_saude_series(receita)
    assert result["indice"] >= 0


# 5. RMSE None vs definido
def test_rmse_none():
    receita = np.array([100, 200, 300])
    result = calcular_indice_saude_series(receita, rmse=None)
    assert result["indice"] >= 0


def test_rmse_valido():
    receita = np.array([100, 200, 300])
    result = calcular_indice_saude_series(receita, rmse=50)
    assert result["indice"] >= 0


# 6. Preset inválido
def test_preset_invalido():
    receita = np.array([100, 200, 300])
    with pytest.raises(ValueError):
        calcular_indice_saude_series(receita, preset="inexistente")


# 7. Pesos inválidos (soma != 1)
def test_pesos_invalidos():
    receita = np.array([100, 200, 300])
    pesos = {
        "crescimento": 0.5,
        "volatilidade": 0.5,
        "momentum": 0.5,
        "erro_modelo": -0.5,
    }
    with pytest.raises(ValueError):
        calcular_indice_saude_series(receita, pesos=pesos)
