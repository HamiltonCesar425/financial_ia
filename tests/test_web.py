import pytest
import requests
from src.financial_ai import web, app
from fastapi.testclient import TestClient

client = TestClient(app)


@pytest.mark.parametrize(
    "status_code, payload, esperado",
    [
        (200, {"data": "ok"}, {"data": "ok"}),  # sucesso
        (404, {"error": "not found"}, {"error": "not found"}),  # recurso não encontrado
        (500, {"error": "server"}, {"error": "server"}),  # erro interno
    ],
)
def test_fetch_data_varios_cenarios(monkeypatch, status_code, payload, esperado):
    class MockResponse:
        def __init__(self, status_code, payload):
            self.status_code = status_code
            self._payload = payload

        def json(self):
            return self._payload

    def mock_get(*args, **kwargs):
        return MockResponse(status_code, payload)

    monkeypatch.setattr(requests, "get", mock_get)
    resultado = web.fetch_data("http://fake-url")
    assert resultado == esperado


def test_fetch_data_timeout(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.exceptions.Timeout

    monkeypatch.setattr(requests, "get", mock_get)

    resultado = web.fetch_data("http://fake-url")
    assert "timeout" in resultado.get("error", "").lower()


def test_home_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}




def test_endpoint_invalido():
    response = client.get("/rota-inexistente")
    assert response.status_code == 404


def test_metodo_invalido():
    response = client.post("/health")
    assert response.status_code in [405, 422]
