from pathlib import Path

from fastapi.testclient import TestClient

from src.domain.diagnosis_service import generate_diagnosis
from src.main import app


client = TestClient(app)


def test_diagnosis_json_endpoint_returns_structured_payload():
    response = client.post(
        "/diagnosis",
        json={
            "receita": 1000,
            "despesas": 400,
            "divida": 150,
            "reserva": 500,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "score": 78,
        "classification": "Saudável",
        "diagnosis": (
            "Seu cenário financeiro demonstra boa solidez "
            "e capacidade de sustentação."
        ),
        "alerts": [
            "Reserva financeira abaixo da cobertura recomendada",
            "Necessidade de monitoramento preventivo",
            "Necessidade de monitoramento preventivo",
        ],
        "recommendations": [
            "Construir reserva equivalente a 3 meses de despesas",
            "Realizar revisão financeira mensal",
            "Realizar revisão financeira mensal",
        ],
    }


def test_diagnosis_json_endpoint_rejects_invalid_payload():
    response = client.post(
        "/diagnosis",
        json={
            "receita": 1000,
            "despesas": 1200,
        },
    )

    assert response.status_code == 422


def test_upload_csv_accepts_portuguese_columns():
    csv_path = Path("tests/data/exemplo.csv")
    files = {
        "file": (csv_path.name, csv_path.read_text(encoding="utf-8"), "text/csv")
    }

    response = client.post("/upload/csv", files=files)

    assert response.status_code == 200
    assert response.json()["score"] == 64
    assert response.json()["classification"] == "Estável"


def test_upload_csv_accepts_english_columns_fixture():
    csv_path = Path("tests/data/diagnosis_upload_valid.csv")
    files = {
        "file": (csv_path.name, csv_path.read_text(encoding="utf-8"), "text/csv")
    }

    response = client.post("/upload/csv", files=files)

    assert response.status_code == 200
    assert response.json()["score"] == 74
    assert response.json()["classification"] == "Estável"


def test_upload_csv_rejects_invalid_extension():
    files = {
        "file": ("dados.txt", "receita,despesas\n1000,300\n", "text/plain")
    }

    response = client.post("/upload/csv", files=files)

    assert response.status_code == 400


def test_upload_csv_rejects_missing_required_columns():
    files = {
        "file": ("dados.csv", "valor,categoria\n1000,receita\n", "text/csv")
    }

    response = client.post("/upload/csv", files=files)

    assert response.status_code == 422
    assert "receita/despesas" in response.json()["detail"]


def test_upload_csv_rejects_invalid_csv_content():
    files = {
        "file": ("dados.csv", 'receita,despesas\n"1000,300\n', "text/csv")
    }

    response = client.post("/upload/csv", files=files)

    assert response.status_code == 400


def test_generate_diagnosis_returns_attention_profile():
    result = generate_diagnosis(
        {
            "receita": 1000,
            "despesas": 800,
            "divida": 700,
            "reserva": 100,
        }
    )

    assert result["score"] == 35
    assert result["classification"] == "Atenção"
    assert result["alerts"] == [
        "Comprometimento elevado da renda",
        "Nível de endividamento acima do ideal",
        "Reserva financeira abaixo da cobertura recomendada",
    ]
    assert result["recommendations"] == [
        "Reduzir despesas variáveis em pelo menos 10%",
        "Priorizar amortização progressiva das dívidas",
        "Construir reserva equivalente a 3 meses de despesas",
    ]


def test_generate_diagnosis_caps_minimum_score_and_classifies_critical():
    result = generate_diagnosis(
        {
            "receita": 1000,
            "despesas": 1000,
            "divida": 2000,
            "reserva": 0,
        }
    )

    assert result["score"] == 0
    assert result["classification"] == "Crítico"


def test_generate_diagnosis_caps_reserve_bonus_and_classifies_stable():
    result = generate_diagnosis(
        {
            "receita": 1000,
            "despesas": 800,
            "divida": 0,
            "reserva": 2400,
        }
    )

    assert result["score"] == 67
    assert result["classification"] == "Estável"


def test_generate_diagnosis_handles_zero_expenses():
    result = generate_diagnosis(
        {
            "receita": 1000,
            "despesas": 0,
            "divida": 0,
            "reserva": 0,
        }
    )

    assert result["score"] == 100
    assert result["classification"] == "Saudável"


def test_generate_diagnosis_rejects_invalid_amounts():
    expected_messages = {
        "receita": "Receita deve ser maior que zero",
        "despesas": "Despesas não podem ser negativas",
        "divida": "Dívida não pode ser negativa",
        "reserva": "Reserva não pode ser negativa",
    }

    for field, expected_message in expected_messages.items():
        data = {
            "receita": 1000,
            "despesas": 300,
            "divida": 0,
            "reserva": 0,
        }
        data[field] = -1

        try:
            generate_diagnosis(data)
        except ValueError as exc:
            assert str(exc) == expected_message
        else:
            raise AssertionError(f"{field} negativo deveria falhar")