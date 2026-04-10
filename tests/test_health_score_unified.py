import pytest
import numpy as np
import pandas as pd

from src.core.health_score import (
    calcular_indice_saude_series,
    calcular_indice_saude,
    calcular_indice_saude_input_simples,
)


def df(valores):
    return pd.DataFrame({"receita": valores})


# =====================================
# INPUT VALIDATION (SÉRIE)
# =====================================
class TestHealthScoreInputValidation:

    @pytest.mark.parametrize(
        "receita, kwargs",
        [
            ([100, 200, 300], {"preset": "invalido"}),
            (
                [100, 200, 300],
                {
                    "pesos": {
                        "crescimento": 0.5,
                        "volatilidade": 0.5,
                        "momentum": 0.5,
                        "erro_modelo": -0.5,
                    }
                },
            ),
        ],
    )
    def test_parametros_invalidos(self, receita, kwargs):
        with pytest.raises(ValueError):
            calcular_indice_saude_series(np.array(receita), **kwargs)


# =====================================
# BUSINESS LOGIC (CORE)
# =====================================
class TestHealthScoreBusinessLogic:

    @pytest.mark.parametrize(
        "valores, rmse",
        [
            ([100, 200, 50, 30], 100),
            ([100, 300, 50, 400, 30], 10),
            ([500, 400, 300, 200], 50),
            ([100, 200, 300, 400], 50),
            ([100, 110, 120, 130], 1),
            ([100, 110, 120, 130], 10000),
            ([1e6, 2e6, 3e6, 4e6], 1000),
        ],
    )
    def test_calculo_indice_valido(self, valores, rmse):
        data = df(valores)
        result = calcular_indice_saude(data, rmse=rmse)

        assert isinstance(result, dict)
        assert "indice" in result
        assert isinstance(result["indice"], (int, float))
        assert 0 <= result["indice"] <= 100


# =====================================
# EDGE CASES (SÉRIE + DATAFRAME)
# =====================================
class TestHealthScoreEdgeCases:

    @pytest.mark.parametrize(
        "valores",
        [
            [1000],  # tamanho 1
            [0, 0, 0],  # zeros
            [0, 100, 200],  # divisão protegida
            [100, 200],  # série curta
        ],
    )
    def test_series_edge_cases(self, valores):
        result = calcular_indice_saude_series(np.array(valores))

        assert isinstance(result, dict)
        assert "indice" in result
        assert 0 <= result["indice"] <= 100

    def test_dataframe_vazio(self):
        with pytest.raises(ValueError):
            calcular_indice_saude(df([]))

    def test_dataframe_sem_coluna(self):
        with pytest.raises(ValueError):
            calcular_indice_saude(pd.DataFrame({"x": [1, 2]}))

    @pytest.mark.parametrize("rmse", ["erro", -1])
    def test_rmse_invalido(self, rmse):
        with pytest.raises(ValueError):
            calcular_indice_saude(df([100, 200, 300]), rmse=rmse)


# =====================================
# INPUT SIMPLES (API)
# =====================================
class TestHealthScoreInputSimples:

    def test_input_negativo(self):
        with pytest.raises(ValueError):
            calcular_indice_saude_input_simples(
                receita=-1000, despesas=500, divida=1000
            )

    def test_cenario_realista(self):
        result = calcular_indice_saude_input_simples(
            receita=1000, despesas=2000, divida=500
        )

        assert isinstance(result, dict)
        assert "score" in result
        assert isinstance(result["score"], (int, float))
        assert result["score"] >= 0

    def test_extremos(self):
        result = calcular_indice_saude_input_simples(
            receita=5000, despesas=2000, divida=10_000_000
        )

        assert isinstance(result, dict)
        assert "score" in result
        assert result["score"] >= 0

    def test_tipo_invalido(self):
        with pytest.raises(ValueError):
            calcular_indice_saude_input_simples(
                receita="5000", despesas=2000, divida=1000
            )
