import pandas as pd

from run_backtest import select_optimal_k, run_out_of_sample_backtest
from src.simulation.simulator import gerar_cenario
from src.models.markov_regime import MarkovRegimeModel


def single_run(seed):

    df = gerar_cenario(meses=500, seed=seed)
    df["market_return"] = df["receita"].pct_change()
    df = df.dropna().reset_index(drop=True)

    train_size = int(len(df) * 0.7)
    train = df.iloc[:train_size]
    test  = df.iloc[train_size:]

    best_k = select_optimal_k(train["market_return"])

    model = MarkovRegimeModel(n_states=best_k)
    model.fit(train["market_return"], index_signal=None)

    results = run_out_of_sample_backtest(model, train, test)

    strategy_sharpe = results["strategy_return"].mean() / results["strategy_return"].std()
    bh_sharpe = results["market_return"].mean() / results["market_return"].std()

    return best_k, strategy_sharpe, bh_sharpe


def monte_carlo(n_sim=80):

    output = []

    for i in range(n_sim):
        print(f"Simulação {i+1}/{n_sim}")
        best_k, strat_sharpe, bh_sharpe = single_run(seed=i)

        output.append((best_k, strat_sharpe, bh_sharpe))

    df_results = pd.DataFrame(
        output,
        columns=["best_k", "sharpe_strategy", "sharpe_bh"]
    )

    return df_results


if __name__ == "__main__":

    results = monte_carlo(n_sim=80)

    print("\n===== RESULTADOS GERAIS =====")
    print(results.describe())

    print("\nFrequência de escolha de k:")
    print(results["best_k"].value_counts())