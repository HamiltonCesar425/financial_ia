from prometheus_client import Counter, Histogram

# Total de requisições de previsão
prediction_requests = Counter(
    "financial_ia_predictions_total",
    "Total number of prediction requests"
)

# Latência das previsões
prediction_latency = Histogram(
    "financial_ia_prediction_latency_seconds",
    "Latency of prediction requests",
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2, 5)
)

# Distribuição dos estados previstos pelo modelo
model_state_counter = Counter(
    "financial_ia_model_state_total",
    "Total predictions by financial state",
    ["state"]

)

# Contador de requisições
http_requests_total = Counter(
    "financial_ia_http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status"]
)

# Latência HTTP
http_request_latency = Histogram(
    "financial_ia_http_request_latency_seconds",
    "HTTP requests latency",
    ["method", "endpoint"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2, 5)
)   

# contador de erros

http_errors_total = Counter(
    "financial_ia_http_errors_total",
    "Total number of HTTP errors",
    ["method", "endpoint", "status"]
)

