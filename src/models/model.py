import os
import joblib
import numpy as np
import pandas as pd

from typing import Tuple, List
from sklearn.linear_model import LinearRegression
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error


# ==============================================================================
# Paths
# ==============================================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "modelo_receita.pkl")


# ==============================================================================
# Feature Engineering
# ==============================================================================

class FeatureEngineer(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        if "data" not in X.columns or "receita" not in X.columns:
            raise ValueError("DataFrame deve conter colunas 'data' e 'receita'.")

        df = X.copy()
        df = df.sort_values("data")

        df["lag1"] = df["receita"].shift(1)
        df["media_movel_3"] = df["receita"].rolling(3).mean()
        df["crescimento_pct"] = df["receita"].pct_change()

        df = df.dropna().reset_index(drop=True)

        return df[["lag1", "media_movel_3", "crescimento_pct"]]


# ==============================================================================
# Validação
# ==============================================================================

def validar_modelo(df: pd.DataFrame) -> Tuple[float, float]:

    if len(df) < 10:
        raise ValueError("Dados insuficientes para validação temporal.")

    fe = FeatureEngineer()
    X = fe.fit_transform(df)

    # y alinhado após dropna das features
    y = df.sort_values("data")["receita"].iloc[-len(X):].reset_index(drop=True)

    tscv = TimeSeriesSplit(n_splits=3)

    maes = []
    rmses = []

    for train_idx, test_idx in tscv.split(X):

        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

        model = LinearRegression()
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        maes.append(mean_absolute_error(y_test, y_pred))
        rmses.append(np.sqrt(mean_squared_error(y_test, y_pred)))

    return float(np.mean(maes)), float(np.mean(rmses))


# ==============================================================================
# Treinamento
# ==============================================================================

def treinar_modelo(df: pd.DataFrame) -> Tuple[LinearRegression, FeatureEngineer]:

    fe = FeatureEngineer()
    X = fe.fit_transform(df)
    y = df.sort_values("data")["receita"].iloc[-len(X):].reset_index(drop=True)

    model = LinearRegression()
    model.fit(X, y)

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump((model, fe), MODEL_PATH)

    return model, fe


# ==============================================================================
# Carregamento inteligente
# ==============================================================================

def carregar_ou_treinar(df: pd.DataFrame) -> Tuple[LinearRegression, FeatureEngineer, float, float]:

    mae, rmse = validar_modelo(df)

    if os.path.exists(MODEL_PATH):
        model, fe = joblib.load(MODEL_PATH)
    else:
        model, fe = treinar_modelo(df)

    return model, fe, mae, rmse


# ==============================================================================
# Previsão Recursiva (3 meses)
# ==============================================================================

def prever_3_meses(
    modelo: LinearRegression,
    fe: FeatureEngineer,
    df: pd.DataFrame
) -> List[float]:

    previsoes = []
    df_temp = df.copy()

    for _ in range(3):

        X_temp = fe.transform(df_temp)

        if X_temp.empty:
            raise ValueError("Dados insuficientes para gerar previsão.")

        previsao = modelo.predict(X_temp.tail(1))
        valor_previsto = float(previsao[-1])

        previsoes.append(valor_previsto)

        # Simulação recursiva
        nova_linha = df_temp.iloc[-1:].copy()
        nova_linha["receita"] = valor_previsto
        nova_linha["data"] = pd.to_datetime(nova_linha["data"]) + pd.DateOffset(months=1)

        df_temp = pd.concat([df_temp, nova_linha], ignore_index=True)

    return previsoes
