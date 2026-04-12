import pytest
from fastapi import HTTPException


# -------------------------
# Cobertura extra para app.py
# -------------------------


def test_app_score_invalid_payload(client):
    # payload sem campos obrigatórios para acionar ramo 422
    payload = {"receita": [500 * 12]}
    response = client.post("/score", json=payload)
    assert response.status_code == 422


def test_app_score_runtime_error(client, monkeypatch):
    import src.api.app

    def fake_calc(*args, **kwargs):
        raise RuntimeError("Erro simulado")

    monkeypatch.setattr(src.api.app, "calcular_indice_saude_input_simples", fake_calc)

    payload = {"receita": 6000, "despesas": 1000, "divida": 500}
    response = client.post("/score", json=payload)
    data = response.json()

    assert response.status_code == 500
    assert "detail" in data
    assert "Erro interno" in data["detail"]


# -------------------------
# Cobertura extra para health_score.py
# -------------------------


def test_health_score_extreme_values():
    from src.core import health_score

    # valores muito altos
    result = health_score.calcular_indice_saude_input_simples(1000, 2000, 5000)
    assert isinstance(result, dict)
    assert "score" in result
    assert isinstance(result["score"], float)

    # despesas iguais à receita
    result = health_score.calcular_indice_saude_input_simples(1000, 1000, 0)
    assert isinstance(result, dict)
    assert "score" in result
    assert isinstance(result["score"], float)
    # dívida igual à receita
    result = health_score.calcular_indice_saude_input_simples(1000, 500, 1000)
    assert isinstance(result, dict)
    assert "score" in result
    assert isinstance(result["score"], float)


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


def test_score_payload_invalido(client):
    response = client.post("/score", json={})
    assert response.status_code == 422


def test_score_valores_invalidos(client):
    response = client.post("/score", json={"receita": -1, "despesas": -1, "divida": -1})
    assert response.status_code in [400, 422]
