import pandas as pd
import pytest

from src.core.health_score import calcular_indice_saude


def test_dataframe_sem_receita_deve_falhar():
    df = pd.DataFrame(
        {
            "renda": [1000, 2000],
        }
    )

    with pytest.raises(ValueError, match="receita"):
        calcular_indice_saude(df)


# ==================================================================
# Teste de df vazio
# ==================================================================
def test_dataframe_vazio_deve_falhar():
    df = pd.DataFrame()

    with pytest.raises(ValueError):
        calcular_indice_saude(df)


# ===================================================================
# Teste de input degenerado
# ===================================================================

import numpy as np


def test_fluxo_degenerado_cobre_branches_internos():
    df = pd.DataFrame(
        {
            "receita": [0, 0, 0, 0, 0, 0, 0],
            "despesas": [np.nan] * 7,
            "divida": [np.inf] * 7,
        }
    )

    result = calcular_indice_saude(df, rmse=0)
    score = result["indice"]

    assert 0 <= score <= 100
