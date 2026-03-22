import time

from src.engine.calculation_engine import FinancialHealthEngine
from src.api.schemas import ReceitaInput, ScoreResponse

from src.observability.metrics import model_state_counter

engine = FinancialHealthEngine()


def predict(data: ReceitaInput) -> ScoreResponse:
    start = time.time()

    try:
        result = engine.predict(data)

        # Métrica de negócio (válida aqui)
        model_state_counter.labels(
            classification=result["classification"]
        ).inc()

        return result

    finally:
        # Latência de modelo (não de request HTTP)
        pass
    
