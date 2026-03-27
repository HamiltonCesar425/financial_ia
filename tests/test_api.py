from fastapi.testclient import TestClient
from src.api.app import app

client = TestClient(app)


def test_endpoint_score():
    response = client.post(
        "/score",
        json={
            "renda": 5000,
            "despesas": 3000,
            "divida": 10000
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "score" in data
    assert "classificacao" in data
    assert "recomendacao" in data
    