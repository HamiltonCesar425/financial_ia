from fastapi import FastAPI
from src.api.app import router
from src.observability.http_metrics_middleware import PrometheusHTTPMiddleware
import os

app = FastAPI(
    title="Financial IA API",
    description="API de avaliação de saúde financeira com classificação e recomendação automática",
    version="1.0.0",
)

# Middleware de métricas
if os.getenv("ENABLE_METRICS", "true").lower() == "true":
    app.add_middleware(PrometheusHTTPMiddleware)

# Inclui o router
app.include_router(router)
