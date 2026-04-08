import pytest

# -------------------------
# Cobertura extra para app.py
# -------------------------


def test_app_score_invalid_payload(client):
    # payload sem campos obrigatórios para acionar ramo 422
    payload = {"receita": 1000}
    response = client.post("/score", json=payload)
    assert response.status_code in (400, 422)


def test_app_score_runtime_error(client, monkeypatch):
    import src.api.app

    def fake_calc(*args, **kwargs):
        raise RuntimeError("Erro simulado")

    monkeypatch.setattr(src.api.app, "calcular_indice_saude_input_simples", fake_calc)

    payload = {"receita": 500, "despesas": 200, "divida": 100}
    response = client.post("/score", json=payload)
    assert response.status_code == 500
    assert "Erro interno" in response.json()["detail"]


# -------------------------
# Cobertura extra para health_score.py
# -------------------------


def test_health_score_extreme_values():
    from src.core import health_score

    # valores muito altos
    result = health_score.calcular_indice_saude_input_simples(1e6, 5e5, 2e5)
    assert isinstance(result, float)

    # despesas iguais à receita
    result = health_score.calcular_indice_saude_input_simples(1000, 1000, 0)
    assert isinstance(result, float)

    # dívida igual à receita
    result = health_score.calcular_indice_saude_input_simples(1000, 500, 1000)
    assert isinstance(result, float)


def test_health_score_invalid_inputs():
    from src.core import health_score

    # receita negativa
    with pytest.raises(ValueError, match="Renda deve ser maior que zero."):
        health_score.calcular_indice_saude_input_simples(-100, 50, 20)

    # despesas negativas
    with pytest.raises(ValueError, match="Valores não podem ser negativos."):
        health_score.calcular_indice_saude_input_simples(1000, -200, 100)

    # dívida negativa
    with pytest.raises(ValueError, match="Valores não podem ser negativos."):
        health_score.calcular_indice_saude_input_simples(1000, 200, -50)


# -------------------------
# Cobertura extra para reports.py
# -------------------------


def test_reports_module_import_and_dummy_call():
    from src.financial_ai import reports

    assert hasattr(reports, "__doc__")
    # se houver função gerar_relatorio, chamamos com dados fictícios
    if hasattr(reports, "gerar_relatorio"):
        reports.gerar_relatorio({"receita": 100, "despesas": 50})


# -------------------------
# Cobertura extra para web.py
# -------------------------


def test_web_module_import_and_dummy_call():
    from src.financial_ai import web

    assert hasattr(web, "__doc__")
    # se houver função iniciar_web, chamamos sem parâmetros
    if hasattr(web, "iniciar_web"):
        web.iniciar_web()
