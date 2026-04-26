from pathlib import Path

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
    csv_path = Path("tests/data/exemplo.csv")
    files = {
        "file": (csv_path.name, csv_path.read_text(encoding="utf-8"), "text/csv")
    }

    response = client.post("/upload/csv", files=files)

    assert response.status_code == 200
    assert response.json()["score"] == 40


def test_upload_csv_accepts_english_columns_fixture():
    csv_path = Path("tests/data/diagnosis_upload_valid.csv")
    files = {
        "file": (csv_path.name, csv_path.read_text(encoding="utf-8"), "text/csv")
    }

    response = client.post("/upload/csv", files=files)

    assert response.status_code == 200
    assert response.json()["score"] == 56


def test_upload_csv_rejects_invalid_extension():
    files = {
        "file": ("dados.txt", "receita,despesas\n1000,300\n", "text/plain")
    }

    response = client.post("/upload/csv", files=files)

    assert response.status_code == 400
