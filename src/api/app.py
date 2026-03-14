#src/api/app.py

import pandas as pd
from fastapi import FastAPI, Response
from typing import List

from prometheus_client import generate_latest, make_asgi_app
from src.observability.http_metrics_middleware import PrometheusHTTPMiddleware

from src.api.schemas import ReceitaInput, ScoreResponse
from src.core.logging import setup_logging
from src.services.prediction_service import predict


logger = setup_logging()
logger.info("API inicializada")

app = FastAPI(
    title="Financial IA",
    description="API de avaliação de saúde financeira empresarial",
    version="1.0.0"
)

# Exportador Prometheus
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

app.add_middleware(PrometheusHTTPMiddleware)


@app.post("/predict", response_model=ScoreResponse)
def run_prediction(receitas: List[ReceitaInput]):

    resultados = []

    for payload in receitas:

        df = pd.DataFrame({
            "receita": payload.receita
        })

        state = predict(df)

        resultados.append(state)

    return {"resultados": resultados}
