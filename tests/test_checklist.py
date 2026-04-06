import pytest
from src.financial_ai import etl, reports, ml, web

# -------------------------------
# 🟢 Camada de Entrada de Dados
# -------------------------------

def test_upload_csv():
    data = etl.load_csv("tests/data/exemplo.csv")
    assert data is not None
    assert "receitas" in data.columns
    assert "despesas" in data.columns

def test_invalid_data_validation():
    with pytest.raises(ValueError):
        etl.load_csv("tests/data/dados_invalidos.csv")

# -------------------------------
# 🟡 Pipeline de Processamento
# -------------------------------

def test_etl_cleaning_and_categorization():
    data = etl.load_csv("tests/data/exemplo.csv")
    clean_data = etl.clean_and_categorize(data)
    assert "categoria" in clean_data.columns
    assert clean_data.isnull().sum().sum() == 0

def test_fluxo_caixa_report_generation():
    data = etl.load_csv("tests/data/exemplo.csv")
    report = reports.generate_fluxo_caixa(data)
    assert "saldo_final" in report
    assert isinstance(report["saldo_final"], (int, float))

def test_ml_prediction_output():
    data = etl.load_csv("tests/data/exemplo.csv")
    prediction = ml.predict_fluxo_caixa(data)
    assert len(prediction) > 0
    assert all(isinstance(val, (int, float)) for val in prediction)

# -------------------------------
# 🔵 Camada Web
# -------------------------------

def test_api_healthcheck():
    client = web.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_dashboard_rendering():
    client = web.test_client()
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert "Fluxo de Caixa" in response.text

# -------------------------------
# 🟣 Testes de Integração
# -------------------------------

def test_end_to_end_pipeline():
    data = etl.load_csv("tests/data/exemplo.csv")
    clean_data = etl.clean_and_categorize(data)
    report = reports.generate_fluxo_caixa(clean_data)
    prediction = ml.predict_fluxo_caixa(clean_data)

    assert "saldo_final" in report
    assert len(prediction) > 0
    assert report["saldo_final"] + prediction[-1] >= 0
