import time
from fastapi import FastAPI, Response

from prometheus_client import generate_latest
from src.observability.http_metrics_middleware import PrometheusHTTPMiddleware

from src.api.schemas import ReceitaInput, ScoreResponse
from src.core.logging import setup_logging
from src.services.prediction_service import predict as predict_service

from src.observability.metrics import (
    REQUEST_COUNT,
    REQUEST_LATENCY,
    PREDICTION_COUNT,
    PREDICTION_ERRORS
)

print(">>> APP.PY REAL CARREGADO <<<")

logger = setup_logging()
logger.info("API inicializada")

app = FastAPI(
    title="Financial IA",
    description="API de avaliação de saúde financeira empresarial",
    version="1.0.0"
)

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")

app.add_middleware(PrometheusHTTPMiddleware)


@app.post("/financial-health-score", response_model=ScoreResponse)
def financial_health_score(data: ReceitaInput):

    REQUEST_COUNT.inc()
    start_time = time.time()

    try:
        prediction = predict_service(data.receita)

        PREDICTION_COUNT.inc()

        return {
            "score": prediction,
            "classification": "unknown",
            "pillars": {},
            "metadata": {}
        }

    except Exception:
        PREDICTION_ERRORS.inc()
        logger.exception("Erro durante predição")
        raise

    finally:
        REQUEST_LATENCY.observe(time.time() - start_time)
