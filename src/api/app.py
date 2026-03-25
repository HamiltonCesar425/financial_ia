import time
import src.services.prediction_service as prediction_service
from fastapi import FastAPI, Response, HTTPException

from prometheus_client import generate_latest
from src.observability.http_metrics_middleware import PrometheusHTTPMiddleware

from src.api.schemas import ReceitaInput, ScoreResponse
from src.core.logging import setup_logging


from src.observability.metrics import (
    prediction_count,
    prediction_errors,
    model_state_counter
)

logger = setup_logging()
logger.info("API inicializada")

app = FastAPI(
    title="Financial IA",
    description="API de avaliação de saúde financeira empresarial",
    version="1.0.0"
)


# 🔹 Endpoint de métricas (Prometheus)
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")


# 🔹 Middleware HTTP (responsável por métricas HTTP)
app.add_middleware(PrometheusHTTPMiddleware)


# 🔹 Endpoint principal
@app.post("/financial-health-score", response_model=ScoreResponse)
def financial_health_score(payload: ReceitaInput):
    start_time = time.time()

    try:
        result = prediction_service.predict(payload.receita)

        # 📊 Métricas de sucesso
        prediction_count.inc()
        model_state_counter.labels(state="success").inc()

        return result

    except Exception as e:
        logger.exception("Erro interno na predição")

        # 📊 Métricas de erro
        prediction_errors.inc()
        model_state_counter.labels(state="error").inc()

        raise HTTPException(status_code=500, detail="Erro interno na predição")

    finally:
        elapsed = time.time() - start_time
        logger.info(f"Tempo de execução: {elapsed:.4f}s")
