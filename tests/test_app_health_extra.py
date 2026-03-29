import pytest
import numpy as np
from fastapi.testclient import TestClient
from src.main import app  # agora importamos do main.py
from src.core import health_score

client = TestClient(app)


# ==============================
# Testes extras para app.py
# ==============================
def test_score_payload_invalido():
    payload = {"receita": "texto", "despesas": 3000, "divida": 1000}
    response = client.post("/score", json=payload)
    assert response.status_code == 422


def test_score_payload_faltando_campo():
    payload = {"receita": 5000, "divida": 1000}
    response = client.post("/score", json=payload)
    assert response.status_code == 422


# ==============================
# Testes extras para health_score.py
# ==============================
def test_calculo_series_vazia():
    receita = np.array([])
    with pytest.raises(ValueError, match="Série de receita vazia"):
        health_score.calcular_indice_saude_series(receita)


def test_calculo_series_com_valores_negativos():
    # A função aceita valores negativos, então verificamos apenas se retorna resultado válido
    receita = np.array(
        [1000, -500, 1200, -300, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500]
    )
    resultado = health_score.calcular_indice_saude_series(receita)
    assert isinstance(resultado, dict)
    assert "indice" in resultado
    assert 0 <= resultado["indice"] <= 100


def test_calculo_series_com_pesos_customizados():
    receita = np.array([1000] * 12)
    pesos = {
        "crescimento": 0.4,
        "volatilidade": 0.2,
        "momentum": 0.2,
        "erro_modelo": 0.2,
    }
    resultado = health_score.calcular_indice_saude_series(receita, pesos=pesos)
    assert isinstance(resultado, dict)
    assert "indice" in resultado
    assert 0 <= resultado["indice"] <= 100
