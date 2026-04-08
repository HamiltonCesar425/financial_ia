import pytest
from src.financial_ai import reports
from src.financial_ai.reports import gerar_relatorio


@pytest.mark.parametrize(
    "dados, esperado",
    [
        ({"valores": [1, 2, 3]}, "Relatório válido"),  # fluxo normal
        ({}, "Erro: dados ausentes"),  # dados ausentes
        ({"valores": None}, "Erro: dados inválidos"),  # dados inválidos
    ],
)
def test_gerar_relatorio_varios_cenarios(dados, esperado):
    resultado = reports.gerar_relatorio(dados)
    assert resultado == esperado


def test_gerar_relatorio_excecao():
    with pytest.raises(Exception):
        reports.gerar_relatorio("entrada_invalida")


def test_relatorio_com_dados_minimos():
    result = gerar_relatorio({})
    assert result is not None
