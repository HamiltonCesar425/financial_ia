import pytest
import numpy as np
from src.core import health_score


# ==============================
# Testes de validação de entrada
# ==============================
def test_receita_zero_gera_erro():
    with pytest.raises(ValueError, match="Renda deve ser maior que zero"):
        health_score.calcular_indice_saude_input_simples(
            receita=0, despesas=100, divida=50
        )


def test_despesas_negativas_gera_erro():
    with pytest.raises(ValueError, match="Valores não podem ser negativos"):
        health_score.calcular_indice_saude_input_simples(
            receita=1000, despesas=-100, divida=50
        )


def test_divida_negativa_gera_erro():
    with pytest.raises(ValueError, match="Valores não podem ser negativos"):
        health_score.calcular_indice_saude_input_simples(
            receita=1000, despesas=100, divida=-50
        )


# ==============================
# Testes de cálculo com série temporal
# ==============================

def test_calculo_series_valido():
    receita = np.array([1000] * 12)
    resultado = health_score.calcular_indice_saude_series(receita)
    assert isinstance(resultado, dict)
    assert "indice" in resultado
    assert 0 <= resultado["indice"] <= 100

def test_calculo_series_receita_variada():
    receita = np.array([1000, 1200, 800, 1500, 1300, 1100, 900, 1400, 1600, 1700, 1800, 2000])
    resultado = health_score.calcular_indice_saude_series(receita)
    assert isinstance(resultado, dict)
    assert "indice" in resultado
    assert 0 <= resultado["indice"] <= 100



# ==============================
# Testes de cenários extremos
# ==============================
def test_despesas_maiores_que_receita():
    resultado = health_score.calcular_indice_saude_input_simples(
        receita=1000, despesas=2000, divida=0
    )
    assert resultado < 50  # deve indicar risco


def test_divida_extremamente_alta():
    resultado = health_score.calcular_indice_saude_input_simples(
        receita=1000, despesas=500, divida=100000
    )
    assert resultado < 30  # deve indicar crítico


def test_receita_muito_alta_com_despesas_baixas():
    resultado = health_score.calcular_indice_saude_input_simples(
        receita=100000, despesas=1000, divida=500
    )
    assert resultado > 80  # deve indicar saudável
