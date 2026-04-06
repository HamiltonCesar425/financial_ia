from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

app = FastAPI()

@app.post("/calcular")
async def calcular(request: Request):
    data = await request.json()
    if not data or data.get("dados") is None:
        return {"error": "Invalid request"}, 400
    if "receitas" not in data or "despesas" not in data:
        return {"error": "Missing fields"}, 422
    return {"resultado": data["receitas"] - data.get("despesas", 0)}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/dashboard")
def dashboard():
    return "<h1>Fluxo de Caixa</h1>"

def test_client():
    return TestClient(app)

