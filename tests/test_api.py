from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_endpoint_score_ok():
    payload = {"receita": 5000, "despesas": 3000, "divida": 10000}

    response = client.post("/score", json=payload)

    assert response.status_code == 200

    body = response.json()

    assert "score" in body
    assert "classificacao" in body
    assert "recomendacao" in body

    assert isinstance(body["score"], (int, float))
    assert isinstance(body["classificacao"], str)
    assert isinstance(body["recomendacao"], str)


def test_endpoint_score_valores_limite():
    payload = {
        "receita": 1,  # mínimo válido (> 0)
        "despesas": 0,  # permitido
        "divida": 0,  # permitido
    }

    response = client.post("/score", json=payload)

    assert response.status_code == 200

    body = response.json()
    assert 0 <= body["score"] <= 100


def test_endpoint_score_payload_invalido():
    payload = {}

    response = client.post("/score", json=payload)

    assert response.status_code == 422


def test_endpoint_score_valores_negativos():
    payload = {"receita": -5000, "despesas": -3000, "divida": -10000}

    response = client.post("/score", json=payload)

    assert response.status_code == 422


def test_endpoint_score_valores_none():
    payload = {"receita": None, "despesas": None, "divida": None}

    response = client.post("/score", json=payload)

    assert response.status_code == 422
