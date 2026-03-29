import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.core import health_score
from src.api.app import _classificar

client = TestClient(app)


# ==============================
# Testes de endpoints auxiliares
# ==============================
def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text


# ==============================
# Testes de classificação
# ==============================

def test_classificar_faixas_direto():
    assert _classificar(85) == "Saudável"
    assert _classificar(65) == "Estável"
    assert _classificar(45) == "Risco"
    assert _classificar(20) == "Crítico"



# ==============================
# Testes de erros internos
# ==============================
def test_score_internal_error(monkeypatch, client):

    def fake_calculo(*args, **kwargs):
        raise RuntimeError("Erro simulado")

    monkeypatch.setattr(
        "src.api.app.calcular_indice_saude_input_simples", fake_calculo
    )

    payload = {"receita": 5000, "despesas": 3000, "divida": 10000}
    response = client.post("/score", json=payload)

    assert response.status_code == 500
    assert response.json()["detail"] == "Erro interno na predição"


# ==============================
# Testes diretos em health_score
# ==============================
def test_receita_negativa_gera_erro():
    with pytest.raises(ValueError, match="Renda deve ser maior que zero"):
        health_score.calcular_indice_saude_input_simples(
            receita=-1000, despesas=500, divida=200
        )


def test_calculo_valido():
    resultado = health_score.calcular_indice_saude_input_simples(
        receita=10000, despesas=5000, divida=2000
    )
    assert isinstance(resultado, float)
    assert 0 <= resultado <= 100


def test_calculo_com_valores_limite():
    resultado = health_score.calcular_indice_saude_input_simples(
        receita=1, despesas=0, divida=0
    )
    assert resultado >= 0
