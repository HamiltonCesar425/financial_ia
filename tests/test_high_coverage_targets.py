import math

import pandas as pd
import pytest
import requests

from src.api import app as api_app
from src.api.business_metrics import (
    CLASSIFICACAO_MAP,
    RECOMENDACAO_MAP,
    _normalize_category,
    classificacao_metric,
    recomendacao_metric,
    update_metrics,
)
from src.core.health_score import (
    calcular,
    calcular_indice_saude,
    calcular_indice_saude_input_simples,
    calcular_indice_saude_series,
    classificar_saude,
    gerar_relatorio_saude,
)
from src.financial_ai.etl import clean_and_categorize, load_csv
from src.financial_ai.ml import predict_fluxo_caixa
from src.financial_ai.reports import generate_fluxo_caixa
from src.financial_ai.web import fetch_data, test_client as web_test_client


def _metric_value(metric):
    return metric._value.get()


def test_load_csv_converte_e_retorna_dataframe(tmp_path):
    csv_path = tmp_path / "financeiro.csv"
    csv_path.write_text("receitas,despesas\n100,40\n200,80\n", encoding="utf-8")

    df = load_csv(csv_path)

    assert list(df.columns) == ["receitas", "despesas"]
    assert df["receitas"].tolist() == [100, 200]
    assert df["despesas"].tolist() == [40, 80]
    assert pd.api.types.is_integer_dtype(df["receitas"])
    assert pd.api.types.is_integer_dtype(df["despesas"])


def test_load_csv_rejeita_nulos(tmp_path):
    csv_path = tmp_path / "financeiro_invalido.csv"
    csv_path.write_text("receitas,despesas\n100,\n", encoding="utf-8")

    with pytest.raises(ValueError, match="valores nulos"):
        load_csv(csv_path)


def test_clean_and_categorize_adiciona_categoria():
    data = pd.DataFrame({"receitas": [100, 50], "despesas": [80, 70]})

    resultado = clean_and_categorize(data)

    assert resultado["categoria"].tolist() == ["entrada", "saida"]
    assert "categoria" not in data.columns


def test_predict_fluxo_caixa_retorna_stub_esperado():
    assert predict_fluxo_caixa({"qualquer": "coisa"}) == [1000, 1200, 900]


def test_generate_fluxo_caixa_soma_metricas():
    data = pd.DataFrame({"receitas": [100, 150], "despesas": [40, 70]})

    resultado = generate_fluxo_caixa(data)

    assert resultado == {
        "total_receitas": 250,
        "total_despesas": 110,
        "saldo_final": 140,
        "saldo_medio": 70,
    }


def test_generate_fluxo_caixa_exige_colunas_obrigatorias():
    data = pd.DataFrame({"receita": [100], "despesa": [20]})

    with pytest.raises(ValueError, match="DataFrame deve conter colunas"):
        generate_fluxo_caixa(data)


def test_web_calcular_fluxo_valido():
    client = web_test_client()

    response = client.post("/calcular", json={"dados": True, "receitas": 120, "despesas": 30})

    assert response.status_code == 200
    assert response.json() == {"resultado": 90}


def test_web_calcular_fluxo_invalido_sem_dados():
    client = web_test_client()

    response = client.post("/calcular", json={})

    assert response.status_code == 200
    assert response.json() == [{"error": "Invalid request"}, 400]


def test_web_calcular_fluxo_sem_campos_obrigatorios():
    client = web_test_client()

    response = client.post("/calcular", json={"dados": True})

    assert response.status_code == 200
    assert response.json() == [{"error": "Missing fields"}, 422]


def test_web_dashboard_e_test_client():
    client = web_test_client()

    dashboard = client.get("/dashboard")

    assert dashboard.status_code == 200
    assert "Fluxo de Caixa" in dashboard.text


def test_fetch_data_retorna_status_generico(monkeypatch):
    class MockResponse:
        status_code = 418

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    assert fetch_data("http://fake-url") == {"error": "status 418"}


def test_calcular_endpoint_fluxo_simples_e_ramo_invalido():
    assert api_app.calcular_endpoint({"receita": 150, "despesas": 30}) == {"resultado": 120}

    with pytest.raises(Exception) as exc_info:
        api_app.calcular_endpoint({"receita": "150", "despesas": 30})

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Invalid data"


@pytest.mark.parametrize(
    ("score", "classificacao", "recomendacao"),
    [
        (85, "Saudável", "Mantenha o padrão financeiro atual."),
        (65, "Estável", "Atenção aos gastos variáveis."),
        (45, "Risco", "Reduza despesas e priorize quitação de dívidas."),
        (10, "Crítico", "Risco elevado: reestruture sua vida financeira imediatamente."),
    ],
)
def test_classificacao_e_recomendacao_por_faixa(score, classificacao, recomendacao):
    assert api_app._classificar(score) == classificacao
    assert api_app._gerar_recomendacao(score) == recomendacao


def test_update_metrics_normaliza_strings_com_acentos():
    update_metrics(
        receita=5000,
        despesas=1000,
        divida=300,
        classificacao="Saudável",
        recomendacao="Atenção aos gastos variáveis.",
    )

    assert _metric_value(classificacao_metric) == CLASSIFICACAO_MAP["saudavel"]
    assert _metric_value(recomendacao_metric) == RECOMENDACAO_MAP["atencao aos gastos variaveis."]


def test_update_metrics_rejeita_valores_invalidos():
    with pytest.raises(ValueError, match="Valores financeiros não podem ser negativos"):
        update_metrics(receita=-1, despesas=0, divida=0)

    with pytest.raises(ValueError, match="Classificação inválida"):
        update_metrics(receita=1, despesas=0, divida=0, classificacao="desconhecida")

    with pytest.raises(ValueError, match="Recomendação inválida"):
        update_metrics(receita=1, despesas=0, divida=0, recomendacao="sem-mapeamento")


def test_normalize_category_remove_acentos_e_espacos():
    assert _normalize_category("  Crítico  ") == "critico"


def test_calcular_score_basico_e_limitado_por_volatilidade():
    assert calcular({"receitas": 300, "despesas": 100}) == 200
    assert calcular({"receitas": 500, "despesas": 100, "volatilidade": 0.9}) == 100

    with pytest.raises(ValueError, match="Dados vazios"):
        calcular({})


@pytest.mark.parametrize("rmse", [math.nan, math.inf])
def test_calcular_indice_saude_rejeita_rmse_invalido(rmse):
    with pytest.raises(ValueError, match="RMSE inválido"):
        calcular_indice_saude(pd.DataFrame({"receita": [100, 120, 130]}), rmse=rmse)


def test_calcular_indice_saude_series_rejeita_pesos_nao_numericos():
    pesos = {
        "crescimento": 0.4,
        "volatilidade": 0.2,
        "momentum": "0.2",
        "erro_modelo": 0.2,
    }

    with pytest.raises(ValueError, match="numéricos"):
        calcular_indice_saude_series(pd.Series([100, 110, 120]).to_numpy(), pesos=pesos)


def test_calcular_indice_saude_series_cobre_preset_agressivo():
    resultado = calcular_indice_saude_series(
        pd.Series([100, 90, 95, 105]).to_numpy(),
        rmse=5,
        preset="agressivo",
    )

    assert 0 <= resultado["indice"] <= 100
    assert set(resultado["componentes"]) == {
        "crescimento",
        "volatilidade",
        "momentum",
        "erro_modelo",
    }


def test_input_simples_rejeita_nan_e_bool():
    with pytest.raises(ValueError, match="Receita inválida"):
        calcular_indice_saude_input_simples(math.nan, 100, 50)

    with pytest.raises(ValueError, match="Receita deve ser numérica"):
        calcular_indice_saude_input_simples(True, 100, 50)


@pytest.mark.parametrize(
    ("indice", "esperado"),
    [
        (10, "Crítico"),
        (50, "Instável"),
        (70, "Saudável"),
        (90, "Excelente"),
    ],
)
def test_classificar_saude_faixas(indice, esperado):
    assert classificar_saude(indice) == esperado


def test_classificar_saude_rejeita_valores_invalidos():
    with pytest.raises(ValueError, match="Índice inválido"):
        classificar_saude("90")

    with pytest.raises(ValueError, match="fora do intervalo"):
        classificar_saude(120)


def test_gerar_relatorio_saude_valida_componentes_e_monta_texto():
    with pytest.raises(ValueError, match="Componentes inválidos"):
        gerar_relatorio_saude(80, "Saudável", [])

    relatorio = gerar_relatorio_saude(
        80,
        "Saudável",
        {"crescimento": 70.0, "volatilidade": 80.0},
    )

    assert "Diagnóstico Financeiro" in relatorio
    assert "Índice: 80 (Saudável)" in relatorio
