import pytest
from src.core.health_score import calcular_indice_saude_input_simples


def test_renda_zero():
    with pytest.raises(ValueError):
        calcular_indice_saude_input_simples(0, 1000, 5000)


def test_valores_negativos():
    with pytest.raises(ValueError):
        calcular_indice_saude_input_simples(-1000, 500, 2000)
        