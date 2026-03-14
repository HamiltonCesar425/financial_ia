import time

from src.engine.calculation_engine import FinancialHealthEngine
from src.observability.metrics import (
    prediction_requests,
    prediction_latency,
    model_state_counter
)

engine = FinancialHealthEngine()


def predict(data):

    start = time.time()

    prediction_requests.inc()

    state = engine.predict(data)

    model_state_counter.labels(state=str(state)).inc()

    prediction_latency.observe(time.time() - start)

    return state
