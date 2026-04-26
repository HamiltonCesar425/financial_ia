# src/observability/http_metrics_middleware.py

import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from src.observability.registry import (
    http_request_count,
    http_request_latency,
)


class PrometheusHTTPMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time

        # 🔹 Labels obrigatórios
        method = request.method
        endpoint = request.url.path
        status_code = response.status_code

        # 🔹 Counter
        http_request_count.labels(
            method=method,
            endpoint=endpoint,
            http_status=status_code
        ).inc()

        # 🔹 Latency
        http_request_latency.labels(
            method=method,
            endpoint=endpoint
        ).observe(process_time)

        return response
    
