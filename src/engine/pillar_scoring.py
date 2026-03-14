# src/engine/pillar_scoring.py

def clamp(x, low=0, high=100):
    return max(low, min(high, x))


def score_crescimento(crescimento):
    return clamp(50 + crescimento * 500)


def score_estabilidade(vol):
    return clamp(100 - vol * 1000)


def score_consistencia(tendencia):
    return clamp(50 + tendencia * 500)


def score_resiliencia(drawdown):
    return clamp(100 + drawdown * 100)
