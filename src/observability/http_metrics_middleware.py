import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from src.observability.metrics import (
    http_requests_total,
    http_request_latency,
    http_errors_total
)


class PrometheusHTTPMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        start_time = time.time()

        method = request.method
        endpoint = request.url.path

        try:

            response = await call_next(request)

            status = response.status_code

        except Exception:

            http_errors_total.labels(
                method=method,
                endpoint=endpoint,
                status="500"
            ).inc()

            raise

        latency = time.time() - start_time

        http_request_latency.labels(
            method=method,
            endpoint=endpoint
        ).observe(latency)

        http_requests_total.labels(
            method=method,
            endpoint=endpoint,
            status=status
        ).inc()

        if status >= 400:
            http_errors_total.labels(
                method=method,
                endpoint=endpoint,
                status=status
            ).inc()

        return response
