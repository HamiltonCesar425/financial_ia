import pytest
from src.core.health_score import calcular_indice_saude_input_simples


def test_score_retorna_float():
    score = calcular_indice_saude_input_simples(5000, 3000, 10000)
    assert isinstance(score, float)


def test_score_intervalo_valido():
    score = calcular_indice_saude_input_simples(5000, 3000, 10000)
    assert 0 <= score <= 100


def test_score_variacao_logica():
    score_bom = calcular_indice_saude_input_simples(8000, 2000, 1000)
    score_ruim = calcular_indice_saude_input_simples(3000, 2900, 20000)

    assert score_bom > score_ruim
    