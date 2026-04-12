from fastapi.testclient import TestClient
from src.main import app
from src.api.metrics import receita_metric, despesas_metric, divida_metric

client = TestClient(app)


def get_metric_value(metric):
    """
    Acesso controlado ao valor interno da métrica.
    Encapsula o uso de atributo privado.
    """
    return metric._value.get()


def test_metrics_update():
    payload = {
        "receita": 10000,
        "despesas": 2500,
        "divida": 1000,
    }

    # Estado antes
    receita_before = get_metric_value(receita_metric)
    despesas_before = get_metric_value(despesas_metric)
    divida_before = get_metric_value(divida_metric)

    response = client.post("/score", json=payload)

    # Validação da API
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)
    assert "score" in data

    # Estado depois
    receita_after = get_metric_value(receita_metric)
    despesas_after = get_metric_value(despesas_metric)
    divida_after = get_metric_value(divida_metric)

    # Gauge atualiza o valor atual, não faz incremento acumulado.
    assert receita_after == payload["receita"]
    assert despesas_after == payload["despesas"]
    assert divida_after == payload["divida"]
