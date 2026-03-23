import pandas as pd
from typing import List, Dict, Any
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
    """
    Engine principal responsável por calcular o score de saúde financeira.

    Fluxo:
    - Entrada: lista de receitas (list[float])
    - Processamento: cálculo de métricas + pilares
    - Saída: dict estruturado com score, classificação e metadata
    """

    def __init__(self, window: int = 12):
        self.window = window

    def predict(self, data: List[float]) -> Dict[str, Any]:
        """
        Interface pública do engine.

        Converte dados brutos em DataFrame e executa o pipeline completo.

        Args:
            data (List[float]): Série temporal de receitas

        Returns:
            Dict[str, Any]: Resultado completo do cálculo
        """

        if not isinstance(data, list):
            raise TypeError("Entrada deve ser uma lista de valores numéricos")

        if len(data) < self.window:
            raise ValueError(f"São necessários pelo menos {self.window} pontos de dados")

        try:
            df = pd.DataFrame({"receita": data})
        except Exception as e:
            raise ValueError("Erro ao converter dados para DataFrame") from e

        return self.compute(df)

    def compute(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Executa o pipeline completo de cálculo do score financeiro.

        Args:
            df (pd.DataFrame): DataFrame contendo coluna 'receita'

        Returns:
            Dict[str, Any]: Resultado estruturado
        """

        if "receita" not in df.columns:
            raise ValueError("DataFrame deve conter coluna 'receita'")

        receita = df["receita"].tail(self.window)

        if len(receita) < self.window:
            raise ValueError("Dados insuficientes para cálculo")

        # 🔹 Cálculo de métricas
        metrics = {
            "crescimento": crescimento_medio(receita),
            "volatilidade": volatilidade(receita),
            "tendencia": tendencia_linear(receita),
            "drawdown": drawdown_max(receita)
        }

        # 🔹 Cálculo de pilares
        pillars = {
            k: float(v)
            for k, v in {
                "crescimento": score_crescimento(metrics["crescimento"]),
                "estabilidade": score_estabilidade(metrics["volatilidade"]),
                "consistencia": score_consistencia(metrics["tendencia"]),
                "resiliencia": score_resiliencia(metrics["drawdown"])
            }.items()
        }

        # 🔹 Pesos dos pilares
        weights = {
            "crescimento": 0.30,
            "estabilidade": 0.25,
            "consistencia": 0.25,
            "resiliencia": 0.20
        }

        # 🔹 Score final ponderado
        score_final = sum(pillars[k] * weights[k] for k in pillars)

        # 🔹 Classificação
        classification = classificar(score_final)

        return {
            "score": float(score_final),
            "classification": classification,
            "pillars": pillars,
            "metadata": {
                "window": self.window,
                "data_points": int(len(receita))
            }
        }
    
