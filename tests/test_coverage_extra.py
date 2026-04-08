import pytest


def test_app_import_and_error(client, monkeypatch):
    import src.api.app

    # força erro interno diferente para cobrir ramo de exceção
    def fake_calc(*args, **kwargs):
        raise RuntimeError("Erro simulado")

    monkeypatch.setattr(src.api.app, "calcular_indice_saude_input_simples", fake_calc)

    payload = {"receita": 500, "despesas": 200, "divida": 100}
    response = client.post("/score", json=payload)
    assert response.status_code == 500


def test_health_score_additional_errors():
    from src.core import health_score

    # despesas negativas
    with pytest.raises(ValueError, match="Valores não podem ser negativos."):
        health_score.calcular_indice_saude_input_simples(1000, -200, 100)

    # dívida negativa
    with pytest.raises(ValueError, match="Valores não podem ser negativos."):
        health_score.calcular_indice_saude_input_simples(1000, 200, -50)


def test_reports_module_import():
    from src.financial_ai import reports

    # apenas garante que o módulo carrega
    assert hasattr(reports, "__doc__")


def test_web_module_import():
    from src.financial_ai import web

    # apenas garante que o módulo carrega
    assert hasattr(web, "__doc__")
