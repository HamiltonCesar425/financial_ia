import numpy as np
import pandas as pd

from src.core.health_score import calcular_indice_saude


def test_nan_nao_propaga_no_score():
    df = pd.DataFrame({
        "receita": [5000, np.nan, 4000],
        "despesas": [2000, 1500, np.nan],
        "divida": [10000, 8000, 6000],
    })

    result = calcular_indice_saude(df, rmse=500)
    score = result["indice"]

    assert not np.isnan(score)

#=============================================================
# Entrada com zero (divisão / estabilidade)
#=============================================================

def test_entrada_com_zero_nao_quebra():
    df = pd.DataFrame({
        "receita": [0, 0, 0],
        "despesas": [0, 0, 0],
        "divida": [0, 0, 0],
    })

    result = calcular_indice_saude(df, rmse=500)
    score = result["indice"]

    assert 0 <= score <= 100

#================================================================
# Valores extremos
#================================================================

def test_valores_extremos_sao_controlados():
    df = pd.DataFrame({
        "receita": [1e9, 1e9, 1e9],
        "despesas": [1e9, 1e9, 1e9],
        "divida": [1e12, 1e12, 1e12],
    })

    result = calcular_indice_saude(df, rmse=500)
    score = result["indice"]

    assert 0 <= score <= 100

#================================================================
# Teste explícito (nan_to_num)
#================================================================

def test_nan_to_num_converte_inf_e_nan():
    df = pd.DataFrame({
        "receita": [np.inf, -np.inf, np.nan],
        "despesas": [np.nan, np.inf, -np.inf],
        "divida": [10000, 20000, 30000],
    })

    result = calcular_indice_saude(df, rmse=500)
    score = result["indice"]

    assert np.isfinite(score)
