# src/engine/classification.py

def classificar(score: float) -> str:
    if score < 40:
        return "Crítico"
    elif score < 60:
        return "Atenção"
    elif score < 80:
        return "Saudável"
    else:
        return "Excelente"
    