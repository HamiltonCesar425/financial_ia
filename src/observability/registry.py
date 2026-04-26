# src/observability/registry.py

from prometheus_client import Counter, Histogram

# =========================================================
# 🔹 HTTP METRICS
# =========================================================

http_request_count = Counter(
    name="http_requests_total",
    documentation="Total number of HTTP requests",
    labelnames=["method", "endpoint", "http_status"]
)

http_request_latency = Histogram(
    name="http_request_duration_seconds",
    documentation="HTTP request latency in seconds",
    labelnames=["method", "endpoint"]
)

# =========================================================
# 🔹 BUSINESS METRICS
# =========================================================

prediction_count = Counter(
    name="prediction_total",
    documentation="Total number of predictions"
)

prediction_errors = Counter(
    name="prediction_errors_total",
    documentation="Total number of prediction errors"
)

# =========================================================
# 🔹 MODEL STATE METRICS (CRÍTICO)
# =========================================================

model_state_counter = Counter(
    name="model_state_total",
    documentation="Model state transitions",
    labelnames=["state"]
)

diagnosis_generated = Counter(
    "diagnosis_generated_total",
    "Total de diagnósticos gerados"
)

diagnosis_latency = Histogram(
    "diagnosis_latency_seconds",
    "Tempo de geração do diagnóstico"
)
