import pytest
from src.core.health_score import calcular_indice_saude_input_simples


# 1. Valores negativos
def test_valores_negativos():
    with pytest.raises(ValueError):
        calcular_indice_saude_input_simples(receita=-1000, despesas=500, divida=1000)


# 2. Zero absoluto (divisão / edge)
def test_renda_zero():
    result = calcular_indice_saude_input_simples(receita=0, despesas=0, divida=0)
    assert result is not None


# 3. Despesas maiores que renda (cenário crítico)
def test_despesa_maior_que_renda():
    result = calcular_indice_saude_input_simples(receita=1000, despesas=2000, divida=500)
    assert result["score"] >= 0


# 4. Dívida extremamente alta
def test_divida_extrema():
    result = calcular_indice_saude_input_simples(
        receita=5000, despesas=2000, divida=10_000_000
    )
    assert result is not None


# 5. Tipos inválidos
def test_tipo_invalido():
    with pytest.raises(Exception):
        calcular_indice_saude_input_simples(receita="5000", despesas=2000, divida=1000)
