import os
from src.api.app import app
from src.observability.http_metrics_middleware import PrometheusHTTPMiddleware

# Middleware de métricas
if os.getenv("ENABLE_METRICS", "true").lower() == "true":
    app.add_middleware(PrometheusHTTPMiddleware)
