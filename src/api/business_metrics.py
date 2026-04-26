import unicodedata
from typing import Optional

from prometheus_client import Counter, Histogram, Gauge


# ==========================================
# NAMESPACE PADRÃO
# ==========================================
NAMESPACE = "financial_ai"


# ==========================================
# COUNTERS (PADRÃO RED)
# ==========================================

REQUEST_COUNT = Counter(
    f"{NAMESPACE}_request_count_total",
    "Total de requisições recebidas",
    ["endpoint"],
)

PREDICTION_REQUESTS = Counter(
    f"{NAMESPACE}_prediction_requests_total",
    "Total de requisições de predição",
    ["status"],  # success | error
)

CLASSIFICATION_COUNTER = Counter(
    f"{NAMESPACE}_prediction_classification_total",
    "Distribuição de classificações",
    ["classificacao"],
)

RECOMMENDATION_COUNTER = Counter(
    f"{NAMESPACE}_prediction_recommendation_total",
    "Distribuição de recomendações",
    ["recomendacao"],
)


# ==========================================
# HISTOGRAMS (CORRETO PARA DISTRIBUIÇÃO)
# ==========================================

PREDICTION_LATENCY = Histogram(
    f"{NAMESPACE}_prediction_latency_seconds",
    "Tempo de execução do endpoint",
    ["endpoint"],
)

RECEITA_HIST = Histogram(
    f"{NAMESPACE}_receita_distribution",
    "Distribuição de receita",
    buckets=(0, 1000, 5000, 10000, 50000, 100000, float("inf")),
)

DESPESAS_HIST = Histogram(
    f"{NAMESPACE}_despesas_distribution",
    "Distribuição de despesas",
    buckets=(0, 1000, 5000, 10000, 50000, 100000, float("inf")),
)

DIVIDA_HIST = Histogram(
    f"{NAMESPACE}_divida_distribution",
    "Distribuição de dívida",
    buckets=(0, 1000, 5000, 10000, 50000, 100000, float("inf")),
)


# ==========================================
# LEGACY METRICS (COMPATIBILIDADE COM TESTES)
# ==========================================

receita_metric = Gauge(
    f"{NAMESPACE}_receita",
    "Receita da empresa (legacy)",
)

despesas_metric = Gauge(
    f"{NAMESPACE}_despesas",
    "Despesas da empresa (legacy)",
)

divida_metric = Gauge(
    f"{NAMESPACE}_divida",
    "Dívida da empresa (legacy)",
)

classificacao_metric = Gauge(
    f"{NAMESPACE}_classificacao",
    "Classificação financeira (legacy)",
)

recomendacao_metric = Gauge(
    f"{NAMESPACE}_recomendacao",
    "Recomendação financeira (legacy)",
)


# ==========================================
# MAPS (VALIDAÇÃO E TESTES)
# ==========================================

CLASSIFICACAO_MAP = {
    "critico": 0,
    "risco": 1,
    "instavel": 1,
    "regular": 1,
    "estavel": 2,
    "saudavel": 3,
    "boa": 3,
    "excelente": 4,
}

RECOMENDACAO_MAP = {
    "reduzir_custos": 0,
    "reduza despesas e priorize quitacao de dividas.": 0,
    "manter": 1,
    "mantenha o padrao financeiro atual.": 1,
    "atencao aos gastos variaveis.": 2,
    "expandir": 3,
    "risco elevado: reestruture sua vida financeira imediatamente.": 3,
}


# ==========================================
# FUNÇÃO CENTRAL DE ATUALIZAÇÃO
# ==========================================

def update_metrics(
    *,
    receita: float,
    despesas: float,
    divida: float,
    classificacao: Optional[str] = None,
    recomendacao: Optional[str] = None,
) -> None:
    """
    Atualiza métricas de forma compatível com Prometheus e testes existentes.

    Estratégia:
    - Histogram: distribuição (produção)
    - Counter + labels: categórico (padrão Prometheus)
    - Gauge: compatibilidade com testes legacy
    """

    # --------------------------
    # Validação
    # --------------------------
    if receita < 0 or despesas < 0 or divida < 0:
        raise ValueError("Valores financeiros não podem ser negativos")

    # --------------------------
    # HISTOGRAM (produção)
    # --------------------------
    RECEITA_HIST.observe(receita)
    DESPESAS_HIST.observe(despesas)
    DIVIDA_HIST.observe(divida)

    # --------------------------
    # LEGACY GAUGE (testes)
    # --------------------------
    receita_metric.set(receita)
    despesas_metric.set(despesas)
    divida_metric.set(divida)

    # --------------------------
    # Classificação
    # --------------------------
    if classificacao is not None:
        classificacao_key = _normalize_category(classificacao)

        if classificacao_key not in CLASSIFICACAO_MAP:
            raise ValueError(f"Classificação inválida: {classificacao}")

        CLASSIFICATION_COUNTER.labels(
            classificacao=classificacao_key
        ).inc()

        classificacao_metric.set(CLASSIFICACAO_MAP[classificacao_key])

    # --------------------------
    # Recomendação
    # --------------------------
    if recomendacao is not None:
        recomendacao_key = _normalize_category(recomendacao)

        if recomendacao_key not in RECOMENDACAO_MAP:
            raise ValueError(f"Recomendação inválida: {recomendacao}")

        RECOMMENDATION_COUNTER.labels(
            recomendacao=recomendacao_key
        ).inc()

        recomendacao_metric.set(RECOMENDACAO_MAP[recomendacao_key])


# ==========================================
# NORMALIZAÇÃO
# ==========================================

def _normalize_category(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    normalized = normalized.encode("ascii", "ignore").decode("ascii")
    return normalized.strip().lower()
