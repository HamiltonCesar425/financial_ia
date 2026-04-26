from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


def test_diagnosis_json_endpoint_returns_structured_payload():
    response = client.post("/diagnosis", json={"receita": 1000, "despesas": 400})

    assert response.status_code == 200
    assert response.json() == {
        "score": 60,
        "message": "Situação estável",
        "recommendation": "Otimizar investimentos",
    }


def test_diagnosis_json_endpoint_rejects_invalid_payload():
    response = client.post("/diagnosis", json={"receita": 1000, "despesas": 1200})

    assert response.status_code == 422


def test_upload_csv_accepts_portuguese_columns():
    files = {
        "file": ("dados.csv", "receita,despesas\n1000,300\n500,200\n", "text/csv")
    }

    response = client.post("/upload/csv", files=files)

    assert response.status_code == 200
    assert response.json()["score"] == 67


def test_upload_csv_rejects_invalid_extension():
    files = {
        "file": ("dados.txt", "receita,despesas\n1000,300\n", "text/plain")
    }

    response = client.post("/upload/csv", files=files)

    assert response.status_code == 400
