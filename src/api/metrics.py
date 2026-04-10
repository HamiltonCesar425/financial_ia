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
    "ruim": 0,
    "regular": 1,
    "boa": 2,
    "excelente": 3,
}

RECOMENDACAO_MAP = {
    "reduzir_custos": 0,
    "manter": 1,
    "expandir": 2,
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
        if classificacao not in CLASSIFICACAO_MAP:
            raise ValueError(f"Classificação inválida: {classificacao}")

        classificacao_metric.set(CLASSIFICACAO_MAP[classificacao])

    if recomendacao is not None:
        if recomendacao not in RECOMENDACAO_MAP:
            raise ValueError(f"Recomendação inválida: {recomendacao}")

        recomendacao_metric.set(RECOMENDACAO_MAP[recomendacao])
