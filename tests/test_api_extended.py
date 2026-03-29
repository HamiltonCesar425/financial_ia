from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_ok():
    payload = {"receita": 5000, "despesas": 3000, "divida": 10000}

    response = client.post("/score", json=payload)

    assert response.status_code == 200

    data = response.json()

    # Validação estrutural
    assert "score" in data
    assert "classificacao" in data
    assert "recomendacao" in data

    # Validação de tipos
    assert isinstance(data["score"], (int, float))
    assert isinstance(data["classificacao"], str)
    assert isinstance(data["recomendacao"], str)

    # Validação de domínio
    assert 0 <= data["score"] <= 100


def test_predict_payload_invalido_tipo():
    payload = {"receita": "erro", "despesas": 1000, "divida": 5000}  # tipo inválido

    response = client.post("/score", json=payload)

    assert response.status_code == 422


def test_predict_payload_invalido_estrutura():
    payload = {
        "receita": [],  # inválido: esperado float
        "despesas": 1000,
        "divida": 5000,
    }

    response = client.post("/score", json=payload)

    assert response.status_code == 422
