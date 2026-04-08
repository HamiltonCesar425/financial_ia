# web.py
import requests
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


def fetch_data(url: str) -> dict:
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return {"error": "not found"}
        elif response.status_code == 500:
            return {"error": "server"}
        else:
            return {"error": f"status {response.status_code}"}
    except requests.exceptions.Timeout:
        return {"error": "timeout"}
