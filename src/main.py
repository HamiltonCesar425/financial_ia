import os
from fastapi import FastAPI

from prometheus_fastapi_instrumentator import Instrumentator
from src.api.app import router
from src.observability.http_metrics_middleware import PrometheusHTTPMiddleware


app = FastAPI(
    title="Financial IA API",
    description="API de avaliação de saúde financeira com classificação e recomendação automática",
    version="1.0.0",
)

# Prometheus Instrumentation
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)


# Middleware de métricas
if os.getenv("ENABLE_METRICS", "true").lower() == "true":
    app.add_middleware(PrometheusHTTPMiddleware)

# Inclui o router
app.include_router(router)
