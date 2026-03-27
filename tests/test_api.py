import pytest
from fastapi.testclient import TestClient
from src.api.app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_financial_health_score_erro_interno(monkeypatch):
    client = TestClient(app)

    def mock_predict(*args, **kwargs):
        raise Exception("erro interno")

    monkeypatch.setattr(
        "src.services.prediction_service.predict",
        mock_predict
    )

    payload = {"receita": [1000] * 12}

    response = client.post("/financial-health-score", json=payload)

    assert response.status_code == 500

def test_financial_health_score_erro_interno(monkeypatch):
    from fastapi.testclient import TestClient
    from src.api.app import app

    client = TestClient(app)

    def mock_predict(*args, **kwargs):
        raise Exception("erro interno")

    monkeypatch.setattr(
        "src.services.prediction_service.predict",
        mock_predict
    )

    payload = {"receita": [1000] * 12}

    response = client.post("/financial-health-score", json=payload)

    assert response.status_code == 500


def test_financial_health_score_input_invalido(client):
    payload = {"receita": [1000] * 5}  # inválido (<12)

    response = client.post("/financial-health-score", json=payload)

    assert response.status_code == 422


def test_financial_health_score_payload_vazio(client):
    response = client.post("/financial-health-score", json={})

    assert response.status_code == 422


def test_financial_health_score_tipo_invalido(client):
    payload = {"receita": "invalido"}

    response = client.post("/financial-health-score", json=payload)

    assert response.status_code == 422


def test_score_adapter_endpoint(client):
    payload = {
        "renda": 5000,
        "despesas": 3000,
        "dividas": 10000
    }

    response = client.post("/score", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert "score" in data
    assert "classificacao" in data
    assert "recomendacao" in data


def test_score_adapter_payload_invalido(client):
    payload = {
        "renda": "erro"
    }

    response = client.post("/score", json=payload)

    assert response.status_code == 400
    
