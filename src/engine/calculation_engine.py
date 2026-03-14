# src/engine/calculation_engine.py

import pandas as pd

from .financial_metrics import (
    crescimento_medio,
    volatilidade,
    tendencia_linear,
    drawdown_max
)

from .pillar_scoring import (
    score_crescimento,
    score_estabilidade,
    score_consistencia,
    score_resiliencia
)

from .classification import classificar


class FinancialHealthEngine:

    def __init__(self, window: int = 12):
        self.window = window

    def compute(self, df: pd.DataFrame) -> dict:

        if "receita" not in df.columns:
            raise ValueError("DataFrame deve conter coluna 'receita'")

        receita = df["receita"].tail(self.window)

        if len(receita) < self.window:
            raise ValueError("Dados insuficientes para cálculo")

        metrics = {
            "crescimento": crescimento_medio(receita),
            "volatilidade": volatilidade(receita),
            "tendencia": tendencia_linear(receita),
            "drawdown": drawdown_max(receita)
        }

        pillars = {
            "crescimento": score_crescimento(metrics["crescimento"]),
            "estabilidade": score_estabilidade(metrics["volatilidade"]),
            "consistencia": score_consistencia(metrics["tendencia"]),
            "resiliencia": score_resiliencia(metrics["drawdown"])
        }

        weights = {
            "crescimento": 0.30,
            "estabilidade": 0.25,
            "consistencia": 0.25,
            "resiliencia": 0.20
        }

        score_final = sum(pillars[k] * weights[k] for k in pillars)

        return {
            "score": score_final,
            "classification": classificar(score_final),
            "pillars": pillars,
            "metadata": {
                "window": self.window,
                "data_points": len(receita)
            }
        }
    
    