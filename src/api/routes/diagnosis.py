from src.observability.registry import diagnosis_generated

@app.post("/diagnosis")
def endpoint(payload: dict):
    result = generate_diagnosis(payload)

    diagnosis_generated.inc()

    return result
