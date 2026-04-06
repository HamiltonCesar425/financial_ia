import pytest

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_metrics_endpoint(client):
    response = client.get("/metrics")
    assert response.status_code == 200
    assert response.text != ""

def test_calcular_endpoint_valid(client):
    payload = {"dados": True, "receitas": 1000, "despesas": 400}
    response = client.post("/calcular", json=payload)
    assert response.status_code == 200
    assert response.json()["resultado"] == 600

def test_calcular_endpoint_invalid_json(client):
    response = client.post("/calcular", data="notjson")
    assert response.status_code == 400

def test_calcular_endpoint_missing_fields(client):
    payload = {"dados": True, "receitas": 1000}
    response = client.post("/calcular", json=payload)
    assert response.status_code == 422

def test_score_endpoint_success(client):
    payload = {"receita": 2000, "despesas": 1000, "divida": 500}
    response = client.post("/score", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert "score" in body
    assert "classificacao" in body
    assert "recomendacao" in body

def test_score_endpoint_runtime_error(client, monkeypatch):
    def fake_calc(*args, **kwargs):
        raise RuntimeError("Erro simulado")

    import src.api.app
    monkeypatch.setattr(src.api.app, "calcular_indice_saude_input_simples", fake_calc)

    payload = {"receita": 1000, "despesas": 500, "divida": 200}
    response = client.post("/score", json=payload)
    assert response.status_code == 500
    assert response.json()["detail"] == "Erro interno na predição"

def test_health_score_edge_cases():
    from src.core import health_score

    # receita zero deve levantar erro
    with pytest.raises(ValueError, match="Renda deve ser maior que zero."):
        health_score.calcular_indice_saude_input_simples(0, 0, 0)

    # despesas maiores que receita
    result = health_score.calcular_indice_saude_input_simples(100, 200, 50)
    assert isinstance(result, float)

    # dívida negativa
    result = health_score.calcular_indice_saude_input_simples(1000, 500, -100)
    assert isinstance(result, float)
