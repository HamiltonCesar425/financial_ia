import pandas as pd


def load_csv(path):
    """
    Carrega um arquivo CSV e valida se não há valores nulos.
    Retorna um DataFrame com colunas 'receitas' e 'despesas'.
    """
    df = pd.read_csv(path)
    if df.isnull().values.any():
        raise ValueError(
            f"Dados inválidos: valores nulos em {df.columns[df.isnull().any()].tolist()}"
        )
    df["receitas"] = df["receitas"].astype(int)
    df["despesas"] = df["despesas"].astype(int)
    return df


def clean_and_categorize(data):
    """
    Adiciona coluna 'categoria' ao DataFrame:
    - 'entrada' se receitas >= despesas
    - 'saida' caso contrário
    """
    data = data.copy()
    data["categoria"] = [
        "entrada" if r >= d else "saida"
        for r, d in zip(data["receitas"], data["despesas"])
    ]
    return data
