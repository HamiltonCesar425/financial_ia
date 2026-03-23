import pytest
import numpy as np
import pandas as pd

from src.simulation.simulator import gerar_cenario
from src.core.health_score import (
    calcular_indice_saude,
    classificar_saude,
    gerar_relatorio_saude,
)


# ==============================================================================
# VALIDAÇÕES DE ENTRADA
# ==============================================================================


def test_dataframe_vazio():
    df = pd.DataFrame()

    with pytest.raises(ValueError):
        calcular_indice_saude(df, rmse=100)


def test_dataframe_com_nan_deve_falhar():
    df = gerar_cenario(meses=36)
    df.loc[0, "receita"] = np.nan  # forma correta

    with pytest.raises(ValueError):
        calcular_indice_saude(df, rmse=100)


def test_rmse_invalido():
    df = gerar_cenario(meses=36)

    with pytest.raises(ValueError):
        calcular_indice_saude(df, rmse=-10)


def test_preset_invalido():
    df = gerar_cenario(meses=36)

    with pytest.raises(ValueError):
        calcular_indice_saude(df, rmse=100, preset="invalido")


# ==============================================================================
# PESOS
# ==============================================================================


def test_soma_pesos_invalida():
    df = gerar_cenario(meses=36)

    pesos = {
        "crescimento": 0.5,
        "volatilidade": 0.5,
        "momentum": 0.5,
        "erro_modelo": 0.5,
    }

    with pytest.raises(ValueError):
        calcular_indice_saude(df, rmse=100, pesos=pesos)


def test_pesos_incompletos():
    df = gerar_cenario(meses=36)

    pesos = {"crescimento": 1.0}

    with pytest.raises(ValueError):
        calcular_indice_saude(df, rmse=100, pesos=pesos)


# ==============================================================================
# PROPRIEDADES DO ÍNDICE
# ==============================================================================


def test_indice_nunca_negativo():
    df = gerar_cenario(meses=36)

    resultado = calcular_indice_saude(df, rmse=1e6)

    assert resultado["indice"] >= 0


def test_indice_maximo_limitado():
    df = gerar_cenario(meses=36, receita_inicial=10000, receita_final=100000)

    resultado = calcular_indice_saude(df, rmse=0)

    assert resultado["indice"] <= 100


# ==============================================================================
# COMPORTAMENTO DO MODELO
# ==============================================================================


def test_volatilidade_extrema_reduz_indice():
    df = gerar_cenario(meses=36, volatilidade=20000, seed=42)

    resultado = calcular_indice_saude(df, rmse=500)

    assert resultado["componentes"]["volatilidade"] < 50


def test_rmse_alto_penaliza_indice():
    df = gerar_cenario(meses=36, seed=42)

    baixo_erro = calcular_indice_saude(df, rmse=100)
    alto_erro = calcular_indice_saude(df, rmse=5000)

    assert alto_erro["indice"] < baixo_erro["indice"]


# ==============================================================================
# CLASSIFICAÇÃO
# ==============================================================================


def test_classificacao_limites_exatos():
    assert classificar_saude(39) == "Crítico"
    assert classificar_saude(40) == "Instável"
    assert classificar_saude(59) == "Instável"
    assert classificar_saude(60) == "Saudável"
    assert classificar_saude(74) == "Saudável"
    assert classificar_saude(75) == "Excelente"


def test_classificacao_invalida():
    with pytest.raises(ValueError):
        classificar_saude(-10)

    with pytest.raises(ValueError):
        classificar_saude(200)


# ==============================================================================
# RELATÓRIO
# ==============================================================================


def test_gerar_relatorio():
    componentes = {
        "crescimento": 70,
        "volatilidade": 30,
        "momentum": 80,
        "erro_modelo": 50,
    }

    relatorio = gerar_relatorio_saude(
        indice=65, classificacao="Saudável", componentes=componentes
    )

    assert "Diagnóstico Financeiro" in relatorio
    assert "Saudável" in relatorio


def test_relatorio_componentes_invalidos():
    with pytest.raises(ValueError):
        gerar_relatorio_saude(50, "Saudável", componentes=None)
