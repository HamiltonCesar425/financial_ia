from src.main import app
from fastapi.testclient import TestClient
from src.api.metrics import receita_metric, despesas_metric, divida_metric

client = TestClient(app)


def test_mestrics_update():
    payload = {"empresa": "XPTO", "receita": 10000, "despesas": 50000, "divida": 20000}
    response = client.post("/score", json=payload)
    assert response.status_code == 200

    # Verifica se métricas foram atualizadas
    assert receita_metric._value.get() == 10000
    assert despesas_metric._value.get() == 50000
    assert divida_metric._value.get() == 20000
