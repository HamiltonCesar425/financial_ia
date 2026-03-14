# src/engine/financial_metrics.py

import numpy as np
import pandas as pd


def crescimento_medio(receita: pd.Series) -> float:
    return receita.pct_change().mean()


def volatilidade(receita: pd.Series) -> float:
    return receita.pct_change().std()


def tendencia_linear(receita: pd.Series) -> float:
    x = np.arange(len(receita))
    coef = np.polyfit(x, receita.values, 1)[0]
    return coef / receita.mean()


def drawdown_max(receita: pd.Series) -> float:
    acumulado = receita / receita.iloc[0]
    pico = acumulado.cummax()
    drawdown = (acumulado - pico) / pico
    return drawdown.min()
