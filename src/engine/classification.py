# src/engine/classification.py

def classificar(score: float) -> str:
    if score >= 90:
        return "Excelente"
    elif score >= 75:
        return "Bom"
    elif score >= 50:
        return "Regular"
    else:
        return "Crítico"
    