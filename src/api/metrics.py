import unicodedata

from prometheus_client import Gauge


# ==========================================
# NAMESPACE PADRÃO
# ==========================================
NAMESPACE = "financial_ai"


# ==========================================
# MÉTRICAS NUMÉRICAS (GAUGE)
# ==========================================
receita_metric = Gauge(
    name=f"{NAMESPACE}_receita",
    documentation="Receita da empresa",
)

despesas_metric = Gauge(
    name=f"{NAMESPACE}_despesas",
    documentation="Despesas da empresa",
)

divida_metric = Gauge(
    name=f"{NAMESPACE}_divida",
    documentation="Dívida da empresa",
)


# ==========================================
# MÉTRICAS CATEGÓRICAS (ENCODING NUMÉRICO)
# ==========================================
"""
Prometheus não trabalha com strings diretamente.
Portanto, usamos encoding numérico controlado.
"""

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


classificacao_metric = Gauge(
    name=f"{NAMESPACE}_classificacao",
    documentation="Classificação financeira (codificada numericamente)",
)

recomendacao_metric = Gauge(
    name=f"{NAMESPACE}_recomendacao",
    documentation="Recomendação financeira (codificada numericamente)",
)


# ==========================================
# FUNÇÃO CENTRAL DE ATUALIZAÇÃO
# ==========================================
def update_metrics(
    *,
    receita: float,
    despesas: float,
    divida: float,
    classificacao: str | None = None,
    recomendacao: str | None = None,
) -> None:
    """
    Atualiza todas as métricas de forma centralizada.

    Args:
        receita (float): Receita da empresa
        despesas (float): Despesas da empresa
        divida (float): Dívida da empresa
        classificacao (str, opcional): Classificação financeira
        recomendacao (str, opcional): Recomendação estratégica
    """

    # --------------------------
    # Validação básica
    # --------------------------
    if receita < 0 or despesas < 0 or divida < 0:
        raise ValueError("Valores financeiros não podem ser negativos")

    # --------------------------
    # Atualização numérica
    # --------------------------
    receita_metric.set(receita)
    despesas_metric.set(despesas)
    divida_metric.set(divida)

    # --------------------------
    # Atualização categórica
    # --------------------------
    if classificacao is not None:
        classificacao_key = _normalize_category(classificacao)

        if classificacao_key not in CLASSIFICACAO_MAP:
            raise ValueError(f"Classificação inválida: {classificacao}")

        classificacao_metric.set(CLASSIFICACAO_MAP[classificacao_key])

    if recomendacao is not None:
        recomendacao_key = _normalize_category(recomendacao)

        if recomendacao_key not in RECOMENDACAO_MAP:
            raise ValueError(f"Recomendação inválida: {recomendacao}")

        recomendacao_metric.set(RECOMENDACAO_MAP[recomendacao_key])


def _normalize_category(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    normalized = normalized.encode("ascii", "ignore").decode("ascii")
    return normalized.strip().lower()
