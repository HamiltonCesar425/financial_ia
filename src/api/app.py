import os
import time

from fastapi import FastAPI, Response, HTTPException
from prometheus_client import generate_latest

import src.services.prediction_service as prediction_service

from src.api.schemas import ReceitaInput, ScoreResponse
from src.core.logging import setup_logging

from src.observability.http_metrics_middleware import PrometheusHTTPMiddleware
from src.observability.metrics import (
    prediction_count,
    prediction_errors,
    model_state_counter,
)

logger = setup_logging()
logger.info("API inicializada")

app = FastAPI(
    title="Financial IA API",
    description="Avaliação de saúde financeira empresarial",
    version="1.0.0",
)

# 🔹 Middleware de métricas
if os.getenv("ENABLE_METRICS", "true") == "true":
    app.add_middleware(PrometheusHTTPMiddleware)


# 🔹 Endpoint de métricas
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")


# 🔹 Endpoint principal (mantido para não quebrar testes)
@app.post("/financial-health-score", response_model=ScoreResponse)
def financial_health_score(payload: ReceitaInput) -> ScoreResponse:
    start_time = time.time()

    try:
        result = prediction_service.predict(payload.receita)

        prediction_count.inc()
        model_state_counter.labels(state="success").inc()

        return result

    except Exception:
        logger.exception("Erro interno na predição")

        prediction_errors.inc()
        model_state_counter.labels(state="error").inc()

        raise HTTPException(status_code=500, detail="Erro interno na predição")

    finally:
        elapsed = time.time() - start_time
        logger.info("Tempo de execução: %.4fs", elapsed)


# 🔹 Novo endpoint padronizado (camada de adaptação)
@app.post("/score", response_model=ScoreResponse)
async def score_adapter(payload: ScoreRequest):
    try:
        result = service.calcular_score(payload)

        if result is None:
            raise HTTPException(
                status_code=500,
                detail="Erro interno ao calcular score"
            )

        return result

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    """
    Endpoint simplificado para uso externo.
    Atua como camada de adaptação sem quebrar o core existente.
    """

# 🔹 Função auxiliar (fora do endpoint)
def _gerar_recomendacao(score: float) -> str:
    if score >= 80:
        return "manter estratégia"
    if score >= 60:
        return "reduzir dívidas"
    return "revisar finanças urgentemente"


# 🔹 Novo endpoint padronizado (camada de adaptação)
@app.post("/score", response_model=ScoreResponse)
def score_adapter(payload: dict) -> ScoreResponse:
    """
    Endpoint simplificado para uso externo.
    Atua como camada de adaptação sem quebrar o core existente.
    """
    start_time = time.time()

    try:
        # 🔹 Conversão controlada para o formato esperado
        receita_liquida = payload.get("renda", 0) - payload.get("despesas", 0)

        # 🔹 Série mínima exigida pelo modelo
        receita_series = [receita_liquida] * 12

        adapted_input = ReceitaInput(receita=receita_series)

        result = financial_health_score(adapted_input)

        # 🔹 Métricas
        prediction_count.inc()
        model_state_counter.labels(state="success").inc()

        # 🔹 Normalização do output
        return ScoreResponse(
            score=result["score"],
            classificacao=result.get("classification", "indefinido").lower(),
            recomendacao=_gerar_recomendacao(result["score"]),
        )

    except Exception:
        logger.exception("Erro no adapter /score")

        prediction_errors.inc()
        model_state_counter.labels(state="error").inc()

        raise HTTPException(status_code=400, detail="Payload inválido")

    finally:
        elapsed = time.time() - start_time
        logger.info("Tempo de execução /score: %.4fs", elapsed)

    
