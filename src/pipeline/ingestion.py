import pandas as pd

COLUNA_OBRIGATORIA = "receita"

"""
Valida e padroniza o DataFrame para uso no motor analítico.
"""
def _validar_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    if COLUNA_OBRIGATORIA not in df.columns:
        raise ValueError(f"Coluna obrigatória '{COLUNA_OBRIGATORIA}' não encontrada.")
    df = df.copy()

    df[COLUNA_OBRIGATORIA] = pd.to_numeric(
        df[COLUNA_OBRIGATORIA],
        errors="coerce"
    )

    df = df.dropna(subset=[COLUNA_OBRIGATORIA])

    if df.empty:
        raise ValueError("Nenhum dado válido encontrado após limpeza.")
    
    return df

"""
Carregar e validar arquivo CSV.
"""
def carregar_csv(caminho: str) -> pd.DataFrame:
    df = pd.read_csv(caminho)
    return _validar_dataframe(df)

"""
Carregar e validar arquivo Excel.
"""
def carregar_excel(caminho: str) -> pd.DataFrame:
    df = pd.read_excel(caminho)
    return _validar_dataframe(df)
