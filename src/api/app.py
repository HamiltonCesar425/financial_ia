import time
from fastapi import FastAPI, Response

from prometheus_client import generate_latest
from src.observability.http_metrics_middleware import PrometheusHTTPMiddleware

from src.api.schemas import ReceitaInput, ScoreResponse
from src.core.logging import setup_logging
from src.services.prediction_service import predict as predict_service

from src.observability.metrics import (
    prediction_count,
    prediction_errors,
    model_state_counter
)

print(">>> APP.PY REAL CARREGADO <<<")

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
def financial_health_score(data: ReceitaInput):

    try:
        # 🔹 Métrica de uso do modelo
        model_state_counter.labels(state="inference").inc()

        prediction = predict_service(data.receita)

        prediction_count.inc()

        return prediction

    except Exception:
        prediction_errors.inc()
        logger.exception("Erro durante predição")
        raise
