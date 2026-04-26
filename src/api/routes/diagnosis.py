# src/api/routes/diagnosis.py

import time

import pandas as pd
from fastapi import APIRouter, File, HTTPException, UploadFile

from src.api.schemas import DiagnosisRequest, DiagnosisResponse
from src.domain.diagnosis_service import generate_diagnosis
from src.observability.registry import diagnosis_generated, diagnosis_latency


router = APIRouter(tags=["Diagnosis"])


def _normalize_csv_columns(df: pd.DataFrame) -> pd.DataFrame:
    canonical_map = {
        "income": "receita",
        "expenses": "despesas",
        "receita": "receita",
        "despesas": "despesas",
    }
    normalized_columns = {
        column: canonical_map[column]
        for column in df.columns
        if column in canonical_map
    }

    if {"receita", "despesas"} - set(normalized_columns.values()):
        raise HTTPException(
            status_code=422,
            detail="CSV must contain receita/despesas or income/expenses columns",
        )

    return df.rename(columns=normalized_columns)


@router.post("/diagnosis", response_model=DiagnosisResponse)
def diagnosis_endpoint(payload: DiagnosisRequest) -> DiagnosisResponse:
    start_time = time.perf_counter()

    try:
        result = generate_diagnosis(payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Erro ao gerar diagnóstico",
        ) from exc

    diagnosis_generated.inc()
    diagnosis_latency.observe(time.perf_counter() - start_time)
    return DiagnosisResponse(**result)


@router.post("/upload/csv", response_model=DiagnosisResponse)
async def upload_csv(file: UploadFile = File(...)) -> DiagnosisResponse:
    start_time = time.perf_counter()

    if not file.filename or not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be CSV")

    try:
        df = pd.read_csv(file.file)
        df = _normalize_csv_columns(df)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Invalid CSV file") from exc

    try:
        data = DiagnosisRequest(
            receita=float(df["receita"].sum()),
            despesas=float(df["despesas"].sum()),
        )
        result = generate_diagnosis(data.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=422, detail="Invalid diagnosis data") from exc

    diagnosis_generated.inc()
    diagnosis_latency.observe(time.perf_counter() - start_time)
    return DiagnosisResponse(**result)
