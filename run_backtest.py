 # run_backtest.py

import numpy as np
import pandas as pd

from src.simulation.simulator import gerar_cenario
from src.models.markov_regime import MarkovRegimeModel


# ==========================================================
# Número de parâmetros do HMM Gaussiano
# ==========================================================
def compute_num_params(k, d=2):
    """
    k = número de estados
    d = dimensão da observação (returns + signal)
    """
    return (
        k * (k - 1) +   # transições
        k * d +         # médias
        k * d +         # variâncias
        (k - 1)         # probabilidades iniciais
    )


# ==========================================================
# Seleção de modelo via AIC/BIC
# ==========================================================
def select_optimal_k(train_returns, train_signal, k_range=range(1, 6)):

    results = []

    for k in k_range:

        model = MarkovRegimeModel(n_states=k)

        model.fit(
            returns=train_returns,
            index_signal=train_signal
        )

        # log-likelihood corretamente escalado
        X = pd.concat([train_returns, train_signal], axis=1).dropna()
        X_scaled = model.scaler.transform(X)

        ll = model.model.score(X_scaled)

        T = len(X)
        p = compute_num_params(k, d=X.shape[1])

        aic = 2 * p - 2 * ll
        bic = np.log(T) * p - 2 * ll

        results.append((k, ll, aic, bic))

    results_df = pd.DataFrame(
        results,
        columns=["k", "LogLik", "AIC", "BIC"]
    ).sort_values("BIC")

    print("\n===== Seleção de Modelo =====")
    print(results_df)

    best_k = int(results_df.iloc[0]["k"])
    print(f"\nMelhor modelo segundo BIC: {best_k} estados")

    return best_k


# ==========================================================
# Backtest fora da amostra (SEM LOOK-AHEAD)
# ==========================================================
def run_out_of_sample_backtest(model, train, test):

    strategy_returns = model.apply_regime_strategy(
        test_returns=test["market_return"],
        test_index_signal=test["signal"]
    )

    aligned_test = test.loc[strategy_returns.index]

    # Métricas
    metrics_strategy = model.compute_metrics(strategy_returns)
    metrics_bh = model.compute_metrics(aligned_test["market_return"])

    print("\n===== Estratégia Regime =====")
    print("CAGR  :", round(metrics_strategy["cagr"], 4))
    print("Vol   :", round(metrics_strategy["vol"], 4))
    print("Sharpe:", round(metrics_strategy["sharpe"], 4))

    print("\n===== Buy & Hold =====")
    print("CAGR  :", round(metrics_bh["cagr"], 4))
    print("Vol   :", round(metrics_bh["vol"], 4))
    print("Sharpe:", round(metrics_bh["sharpe"], 4))

    print("\nMatriz de Transição (treino):")
    print(model.transition_matrix())

    return strategy_returns


# ==========================================================
# MAIN
# ==========================================================
def main():

    # ======================================================
    # 1. Gerar cenário estocástico
    # ======================================================
    df = gerar_cenario(meses=500)

    df["market_return"] = df["receita"].pct_change()

    # Exemplo simples de sinal auxiliar
    df["signal"] = df["receita"].rolling(3).mean()

    df = df.dropna()

    # ======================================================
    # 2. Split temporal 70 / 30
    # ======================================================
    train_size = int(len(df) * 0.7)

    train = df.iloc[:train_size].copy()
    test  = df.iloc[train_size:].copy()

    # ======================================================
    # 3. Seleção ótima de estados
    # ======================================================
    best_k = select_optimal_k(
        train_returns=train["market_return"],
        train_signal=train["signal"],
        k_range=range(1, 6)
    )

    # ======================================================
    # 4. Treinar modelo final
    # ======================================================
    final_model = MarkovRegimeModel(n_states=best_k)

    final_model.fit(
        returns=train["market_return"],
        index_signal=train["signal"]
    )

    # Log-likelihood informativo
    X_train = pd.concat(
        [train["market_return"], train["signal"]],
        axis=1
    ).dropna()

    X_test = pd.concat(
        [test["market_return"], test["signal"]],
        axis=1
    ).dropna()

    train_ll = final_model.model.score(
        final_model.scaler.transform(X_train)
    )

    test_ll = final_model.model.score(
        final_model.scaler.transform(X_test)
    )

    print("\nLog-Likelihood por observação:")
    print("Treino:", round(train_ll / len(X_train), 4))
    print("Teste :", round(test_ll / len(X_test), 4))

    # ======================================================
    # 5. Backtest fora da amostra
    # ======================================================
    run_out_of_sample_backtest(
        model=final_model,
        train=train,
        test=test
    )


if __name__ == "__main__":
    main()
    