# markov_regime.py

import numpy as np
import pandas as pd
from hmmlearn.hmm import GaussianHMM
from sklearn.preprocessing import StandardScaler


class MarkovRegimeModel:
    """
    Modelo HMM com política de exposição agressiva (100% / 0%).

    Fluxo correto:
    - Fit no treino
    - Detecta bull_state no treino
    - Aplica regra no teste
    """

    def __init__(self, n_states=2, random_state=42):
        self.n_states = n_states
        self.random_state = random_state

        self.model = GaussianHMM(
            n_components=n_states,
            covariance_type="diag",
            n_iter=2000,
            tol=1e-4,
            min_covar=1e-4,
            random_state=random_state
        )

        self.scaler = StandardScaler()

        self.fitted = False
        self.bull_state = None
        self.bear_state = None

    # ==========================================================
    # FIT (TREINO)
    # ==========================================================

    def fit(self, returns: pd.Series, index_signal: pd.Series):
        """
        Ajusta o HMM apenas no conjunto de treino.
        """

        X = pd.concat([returns, index_signal], axis=1).dropna()
        self.train_index_ = X.index

        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled)

        hidden_states = self.model.predict(X_scaled)

        train_df = pd.DataFrame({
            "return": X.iloc[:, 0],
            "state": hidden_states
        }, index=X.index)

        mean_by_state = train_df.groupby("state")["return"].mean()

        self.bull_state = mean_by_state.idxmax()
        self.bear_state = mean_by_state.idxmin()

        self.fitted = True
        return self

    # ==========================================================
    # PREDIÇÃO DE ESTADOS
    # ==========================================================

    def predict_states(self, returns: pd.Series, index_signal: pd.Series):
        """
        Prediz estados para novos dados (teste).
        """

        if not self.fitted:
            raise RuntimeError("Modelo não ajustado.")

        X = pd.concat([returns, index_signal], axis=1).dropna()
        X_scaled = self.scaler.transform(X)

        states = self.model.predict(X_scaled)

        return pd.Series(states, index=X.index)

    # ==========================================================
    # REGRA DE EXPOSIÇÃO AGRESSIVA
    # ==========================================================

    def apply_regime_strategy(
        self,
        test_returns: pd.Series,
        test_index_signal: pd.Series
    ):
        """
        Aplica política:
        - 100% investido no bull_state
        - 0% no bear_state
        """

        states = self.predict_states(test_returns, test_index_signal)

        aligned_returns = test_returns.loc[states.index]

        strategy_returns = np.where(
            states == self.bull_state,
            aligned_returns,
            0.0
        )

        return pd.Series(strategy_returns, index=states.index)

    # ==========================================================
    # MATRIZ DE TRANSIÇÃO
    # ==========================================================

    def transition_matrix(self):
        if not self.fitted:
            raise RuntimeError("Modelo não ajustado.")

        return pd.DataFrame(
            self.model.transmat_,
            columns=[f"to_{i}" for i in range(self.n_states)],
            index=[f"from_{i}" for i in range(self.n_states)]
        )

    # ==========================================================
    # MÉTRICAS DE PERFORMANCE
    # ==========================================================

    @staticmethod
    def compute_metrics(returns: pd.Series):
        """
        Calcula CAGR, Volatilidade e Sharpe.
        """

        if len(returns) == 0:
            return {"cagr": 0, "vol": 0, "sharpe": 0}

        cumulative = (1 + returns).cumprod()
        total_return = cumulative.iloc[-1]

        periods = len(returns)
        cagr = total_return ** (12 / periods) - 1

        vol = returns.std() * np.sqrt(12)

        sharpe = 0
        if vol != 0:
            sharpe = cagr / vol

        return {
            "cagr": float(cagr),
            "vol": float(vol),
            "sharpe": float(sharpe)
        }