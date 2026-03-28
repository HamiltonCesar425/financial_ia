import os
import time
import pandas as pd

from fastapi import FastAPI, Response, HTTPException
from prometheus_client import generate_latest

from src.core.health_score import (
    calcular_indice_saude_input_simples,
    calcular_indice_saude,
)
from src.api.schemas import ScoreResponse, ScoreRequest
from src.core.logging import setup_logging
from src.observability.http_metrics_middleware import PrometheusHTTPMiddleware
from src.observability.metrics import (
    prediction_count,
    prediction_errors,
    model_state_counter,
)

# ======================================
# Logging
# ======================================
logger = setup_logging()
logger.info("API inicializada")


# ======================================
# App Initialization
# ======================================
app = FastAPI(
    title="Financial IA API",
    description="API de avaliação de saúde financeira com classificação e recomendação automática",
    version="1.0.0",
)


# ======================================
# Middleware (Observabilidade)
# ======================================
if os.getenv("ENABLE_METRICS", "true").lower() == "true":
    app.add_middleware(PrometheusHTTPMiddleware)


# ======================================
# Endpoints auxiliares
# ======================================
@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")


# ======================================
# Lógica de classificação
# ======================================
def _classificar(score: float) -> str:
    if score >= 80:
        return "Saudável"
    if score >= 60:
        return "Estável"
    if score >= 40:
        return "Risco"
    return "Crítico"


def _gerar_recomendacao(score: float) -> str:
    if score >= 80:
        return "Mantenha o padrão financeiro atual."
    if score >= 60:
        return "Atenção aos gastos variáveis."
    if score >= 40:
        return "Reduza despesas e priorize quitação de dívidas."
    return "Risco elevado: reestruture sua vida financeira imediatamente."


# ======================================
# Endpoint principal (CORRIGIDO)
# ======================================
@app.post("/score", response_model=ScoreResponse)
def calcular_score(payload: ScoreRequest) -> ScoreResponse:
    start_time = time.time()

    try:
        # =========================
        # DECISÃO BASEADA NO SCHEMA (CORRETO)
        # =========================
        if payload.data is not None:
            df = pd.DataFrame({"receita": payload.data})
            result = calcular_indice_saude(df)
            score = result["indice"]

        else:
            score = calcular_indice_saude_input_simples(
                renda=payload.renda,
                despesas=payload.despesas,
                divida=payload.divida,
            )

        # =========================
        # CLASSIFICAÇÃO
        # =========================
        classificacao = _classificar(score)
        recomendacao = _gerar_recomendacao(score)

        prediction_count.inc()
        model_state_counter.labels(state="success").inc()

        return ScoreResponse(
            score=round(score, 2),
            classificacao=classificacao,
            recomendacao=recomendacao,
        )

    except ValueError as exc:
        logger.warning("Erro de validação: %s", str(exc))
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    except Exception as exc:
        logger.exception("Erro interno na predição")

        prediction_errors.inc()
        model_state_counter.labels(state="error").inc()

        raise HTTPException(
            status_code=500,
            detail="Erro interno na predição",
        ) from exc

    finally:
        elapsed = time.time() - start_time
        logger.info("Tempo de execução: %.4fs", elapsed)
