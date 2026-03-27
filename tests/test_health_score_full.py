import pytest
import numpy as np
from src.core.health_score import calcular_indice_saude_series, calcular_indice_saude

def test_series_completa():
    receita = np.array([1000, 1300, 1500, 1600])
    result = calcular_indice_saude_series(receita)
    assert "indice" in result
    assert "componentes" in result

def test_serie_vazia():
    with pytest.raises(ValueError):
        calcular_indice_saude_series(np.array([]))
