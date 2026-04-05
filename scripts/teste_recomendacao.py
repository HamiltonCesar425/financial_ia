import requests

BASE_URL = "http://localhost:8000"

# Cenários de teste para forçar cada recomendação
cenarios = [
    {"receita": 8000, "despesas": 2000, "divida": 0},  # Saudável
    {"receita": 5000, "despesas": 3000, "divida": 500},  # Estável
    {"receita": 4000, "despesas": 3500, "divida": 1000},  # Risco
    {"receita": 2000, "despesas": 2500, "divida": 3000},  # Crítico
]

for c in cenarios:
    # Chama o endpoint /score
    resp = requests.post(f"{BASE_URL}/score", json=c)
    data = resp.json()
    print(f"\nCenário: {c}")
    print(f"Classificação: {data['classificacao']}")
    print(f"Recomendação: {data['recomendacao']}")

    # Consulta o endpoint /metrics
    metrics = requests.get(f"{BASE_URL}/metrics").text
    # Filtra apenas a linha da recomendação
    for line in metrics.splitlines():
        if line.startswith("financial_ai_recomendacao"):
            print(f"Valor da métrica: {line}")
