import pytest
from src.simulation.simulator import gerar_cenario

def test_mes_invalido():
    with pytest.raises(ValueError):
        gerar_cenario(meses=1)


def test_receita_invalida():
    with pytest.raises(ValueError):
        gerar_cenario(receita_inicial=-100)


def test_choque_invalido():
    with pytest.raises(ValueError):
        gerar_cenario(choque_em=100)


def test_sem_volatilidade():
    df = gerar_cenario(volatilidade=0)
    assert "receita" in df.columns


