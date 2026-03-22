from fastapi.testclient import TestClient
from src.api.app import app

client = TestClient(app)

def test_financial_health_score():
    payload = {
        "receita": [1000] * 12
    }

    response = client.post("/financial-health-score", json=payload)

    assert response.status_code == 200
    assert "score" in response.json()

def test_invalid_input():
    payload = {
        "receita": [1000] * 5  # inválido (<12)
    }

    response = client.post("/financial-health-score", json=payload)

    assert response.status_code == 422
    