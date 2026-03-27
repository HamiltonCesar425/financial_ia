import pandas as pd
from typing import List, Dict, Any
from src.core.health_score import calcular_indice_saude
from src.engine.calculation_engine import FinancialHealthEngine
from src.observability.metrics import model_state_counter


engine = FinancialHealthEngine()


def predict(data: List[float]) -> Dict[str, Any]:
    """
    Service responsável por orquestrar a predição do modelo.

    - Recebe dados brutos (List[float])
    - Retorna estrutura pronta (dict)
    - Registra métricas de observabilidade
    """

    if not data or not isinstance(data, list):
        raise ValueError("Dados inválidos para predição")

    try:
        result = engine.predict(data)

        model_state_counter.labels(state="success").inc()

        return result

    except Exception:
        model_state_counter.labels(state="error").inc()
        raise
def calcular_score(renda: float, despesas: float, divida: float) -> float:
    if renda < 0 or despesas < 0 or divida < 0:
        raise ValueError("Valores inválidos")

    score = (renda - despesas) / (divida + 1) * 100

    return float(max(0, min(score, 100)))

