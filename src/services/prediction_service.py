from typing import List, Dict, Any

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
