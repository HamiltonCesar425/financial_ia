# src/simulation/simulator.py

import numpy as np
import pandas as pd


def gerar_cenario(
    meses: int = 12,
    receita_inicial: float = 1000.0,
    receita_final: float = 2000.0,
    volatilidade: float = 0.0,
    choque_em: int | None = None,
    intensidade_choque: float = 0.0,
    seed: int | None = None
) -> pd.DataFrame:
    """
    Gera série mensal de receita com:

    - Crescimento linear determinístico
    - Ruído gaussiano opcional
    - Choque percentual aplicado corretamente
    - Reprodutibilidade via seed
    """

    # 🔒 Validações
    if meses < 2:
        raise ValueError("meses deve ser >= 2")

    if receita_inicial <= 0 or receita_final <= 0:
        raise ValueError("Receitas devem ser positivas")

    if volatilidade < 0:
        raise ValueError("volatilidade não pode ser negativa")

    if seed is not None:
        np.random.seed(seed)

    # 📈 Tendência determinística
    tendencia = np.linspace(
        receita_inicial,
        receita_final,
        meses
    )

    # 🔊 Ruído
    if volatilidade > 0:
        ruido = np.random.normal(
            loc=0.0,
            scale=volatilidade,
            size=meses
        )
    else:
        ruido = np.zeros(meses)

    receita = tendencia + ruido

    # 🔒 Evita valores negativos
    receita = np.maximum(receita, 1.0)

    # ⚡ Choque percentual
    if choque_em is not None:
        if not (0 <= choque_em < meses):
            raise ValueError("choque_em fora do intervalo")

        receita[choque_em:] *= (1 + intensidade_choque)

    # 📊 DataFrame final
    df = pd.DataFrame({
        "mes": pd.date_range(
            start="2020-01-01",
            periods=meses,
            freq="ME"
        ),
        "receita": receita
    })

    return df
