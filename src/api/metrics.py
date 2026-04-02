from prometheus_client import Gauge

# DEfinindo métricas customizadas

receita_metric = Gauge("financial_ai_receita", "Receita da empresa")
despesas_metric = Gauge("financial_ai_despesas", "Despesas da empresa")
divida_metric = Gauge("financial_ai_divida", "Dívida da empresa")

