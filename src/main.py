import pandas as pd

from engine.calculation_engine import FinancialHealthEngine
from src.simulation.simulator import gerar_cenario


def main():

    df = gerar_cenario(
        meses=36,
        receita_inicial=20000,
        receita_final=50000,
        volatilidade=2000,
        seed=42
    )

    engine = FinancialHealthEngine(window=12)

    resultado = engine.compute(df)

    print("\n===== FINANCIAL HEALTH SCORE =====\n")

    print("Score:", resultado["score"])
    print("Classificação:", resultado["classification"])

    print("\nPilares:")

    for k, v in resultado["pillars"].items():
        print(f"{k}: {v:.2f}")


if __name__ == "__main__":
    main()

