from dataclasses import dataclass
from typing import List, Dict
import pandas as pd


@dataclass
class BacktestConfig:
    """
    Configuração do backtest walk-forward.
    """
    min_window: int
    horizons: List[int]
    step: int = 1


class MultiHorizonBacktester:
    """
    Backtester walk-forward multi-horizonte.

    Para cada horizonte:
    - Usa janela histórica crescente
    - Calcula índice de saúde
    - Mede retorno futuro
    - Armazena direção real
    """

    def __init__(self, config: BacktestConfig, health_engine):
        self.config = config
        self.health_engine = health_engine

    def run(self, df: pd.DataFrame) -> Dict[int, pd.DataFrame]:

        # =========================
        # Validação mínima
        # =========================
        required_cols = {"date", "receita"}
        if not required_cols.issubset(df.columns):
            raise ValueError(
                f"DataFrame deve conter colunas: {required_cols}"
            )

        df = df.copy()
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date").reset_index(drop=True)

        results: Dict[int, pd.DataFrame] = {}

        # =========================
        # Loop por horizonte
        # =========================
        for horizon in self.config.horizons:

            rows = []

            for i in range(
                self.config.min_window,
                len(df) - horizon,
                self.config.step
            ):

                historical = df.iloc[:i].copy()
                future = df.iloc[i + horizon]

                # Índice calculado com dados até o tempo i
                indice = self.health_engine.compute(historical)

                current_price = df.iloc[i]["receita"]
                future_price = future["receita"]

                retorno_futuro = (
                    future_price - current_price
                ) / current_price

                direcao_real = 1 if retorno_futuro > 0 else 0

                rows.append({
                    "date": df.iloc[i]["date"],
                    "indice": float(indice),
                    "retorno_futuro": float(retorno_futuro),
                    "direcao_real": int(direcao_real)
                })

            results[horizon] = pd.DataFrame(rows)

        return results
    