import pytest
from src.core.health_score import calcular_indice_saude_input_simples


def test_score_retorna_estrutura_valida():
    result = calcular_indice_saude_input_simples(5000, 3000, 10000)

    assert isinstance(result, dict)
    assert "score" in result
    assert isinstance(result["score"], float)


def test_score_intervalo_valido():
    result = calcular_indice_saude_input_simples(5000, 3000, 10000)
    score = result["score"]

    assert 0 <= score <= 100


def test_score_variacao_logica():
    result_bom = calcular_indice_saude_input_simples(8000, 2000, 1000)
    result_ruim = calcular_indice_saude_input_simples(3000, 2900, 20000)

    assert result_bom["score"] > result_ruim["score"]


def test_score_receita_invalida():
    with pytest.raises(ValueError, match="Renda deve ser maior que zero"):
        calcular_indice_saude_input_simples(0, 100, 100)