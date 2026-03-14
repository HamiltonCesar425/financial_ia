import pandas as pd


def gerar_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.sort_values("data")

    df["lag1"] = df["receita"].shift(1)
    df["media_movel_3"] = df["receita"].rolling(3).mean()
    df["crescimento_pct"] = df["receita"].pct_change()

    df = df.dropna().reset_index(drop=True)

    return df
