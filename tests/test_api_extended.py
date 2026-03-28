from fastapi.testclient import TestClient
from src.api.app import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200


def test_predict_ok():
    payload = {
        "data": [100, 110, 120, 130],
        "window": 3
    }

    response = client.post("/score", json=payload)

    assert response.status_code == 200

    body = response.json()
    assert "score" in body or "indice" in body


def test_predict_tipo_invalido():
    payload = {
        "data": "erro"
    }

    response = client.post("/score", json=payload)

    assert response.status_code in [400, 422]


def test_predict_window_invalida():
    payload = {
        "data": [100, 110],
        "window": 10
    }

    response = client.post("/score", json=payload)

    assert response.status_code in [400, 422]
    