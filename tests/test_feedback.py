from fastapi.testclient import TestClient

from src.api.app import app


def test_feedback_endpoint_accepts_minimal_message(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    client = TestClient(app)
    response = client.post("/feedback", json={"message": "Produto claro e útil."})

    assert response.status_code == 200
    assert response.json()["status"] == "received"
    assert (tmp_path / "data" / "feedback.jsonl").exists()


def test_feedback_endpoint_rejects_blank_message(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    client = TestClient(app)
    response = client.post("/feedback", json={"message": "   "})

    assert response.status_code == 422
