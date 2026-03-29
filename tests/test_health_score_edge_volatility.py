import pandas as pd
from src.core.health_score import calcular_indice_saude


def test_volatilidade_com_apenas_um_valor():
    df = pd.DataFrame({"receita": [1000]})

    result = calcular_indice_saude(df)

    assert "indice" in result
    assert result["indice"] >= 0


# ==============================================


def test_receita_com_zeros_e_nan():
    df = pd.DataFrame({"receita": [0, 0, 0, 0, 0, 0]})

    result = calcular_indice_saude(df)

    assert result["indice"] >= 0


# ==============================================


def test_receita_extremamente_volatil():
    df = pd.DataFrame(
        {"receita": [1000, 100000, 10, 50000, 5, 80000, 3, 90000, 2, 100000, 1, 120000]}
    )

    result = calcular_indice_saude(df)

    assert 0 <= result["indice"] <= 100


# ==============================================


def test_score_limite_inferior():
    df = pd.DataFrame({"receita": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]})

    result = calcular_indice_saude(df)

    assert result["indice"] >= 0
