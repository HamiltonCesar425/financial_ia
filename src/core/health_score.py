import numpy as np
import pandas as pd


# ==============================================================================
# PRESETS
# ==============================================================================

PESOS_PRESETS = {
    "balanceado": {
        "crescimento": 0.4,
        "volatilidade": 0.2,
        "momentum": 0.2,
        "erro_modelo": 0.2
    },
    "conservador": {
        "crescimento": 0.25,
        "volatilidade": 0.35,
        "momentum": 0.15,
        "erro_modelo": 0.25
    },
    "agressivo": {
        "crescimento": 0.45,
        "volatilidade": 0.15,
        "momentum": 0.20,
        "erro_modelo": 0.20
    }
}


# ==============================================================================
# FUNÇÕES DE NORMALIZAÇÃO LOGÍSTICA
# ==============================================================================

def logistic_positive(x, center=0.05, steepness=12):
    """Maior é melhor"""
    x = np.nan_to_num(x, nan=0.0, posinf=1e6, neginf=-1e6)
    return 100 / (1 + np.exp(-steepness * (x - center)))


def logistic_negative(x, center=0.10, steepness=12):
    """Menor é melhor"""
    x = np.nan_to_num(x, nan=0.0, posinf=1e6, neginf=-1e6)
    return 100 / (1 + np.exp(steepness * (x - center)))


# ==============================================================================
# VALIDAÇÕES AUXILIARES
# ==============================================================================

def _validar_dataframe(df: pd.DataFrame):
    if df is None or not isinstance(df, pd.DataFrame):
        raise ValueError("Entrada deve ser um DataFrame válido.")

    if df.empty:
        raise ValueError("DataFrame não pode ser vazio.")

    if "receita" not in df.columns:
        raise ValueError("Coluna 'receita' obrigatória.")

    if df["receita"].isna().any():
        raise ValueError("Dados contêm valores NaN na coluna 'receita'.")


def _validar_rmse(rmse):
    if rmse is None:
        return

    if not isinstance(rmse, (int, float)):
        raise ValueError("RMSE deve ser numérico.")

    if np.isnan(rmse) or np.isinf(rmse):
        raise ValueError("RMSE inválido.")

    if rmse < 0:
        raise ValueError("RMSE não pode ser negativo.")


def _validar_pesos(pesos: dict):
    if not isinstance(pesos, dict):
        raise ValueError("Pesos devem ser um dicionário.")

    if not np.isclose(sum(pesos.values()), 1.0):
        raise ValueError("A soma dos pesos deve ser 1.")

    for k in ["crescimento", "volatilidade", "momentum", "erro_modelo"]:
        if k not in pesos:
            raise ValueError(f"Peso ausente: {k}")


# ==============================================================================
# FUNÇÃO PRINCIPAL
# ==============================================================================

def calcular_indice_saude(df, rmse=None, preset="balanceado", pesos=None):

    _validar_dataframe(df)
    _validar_rmse(rmse)

    receita = df["receita"].astype(float)

    # --------------------------------------------------------------------------
    # MÉTRICAS BRUTAS
    # --------------------------------------------------------------------------

    # CAGR
    if len(receita) < 2:
        growth = 0.0
    else:
        n = len(receita) - 1
        vi = receita.iloc[0]
        vf = receita.iloc[-1]

        if vi <= 0 or vf <= 0:
            growth = 0.0
        else:
            growth = (vf / vi) ** (1 / n) - 1

    # Volatilidade
    pct = receita.pct_change().dropna()
    vol = pct.tail(min(6, len(pct))).std(ddof=0) if len(pct) > 0 else 0.0

    # Momentum
    if len(receita) < 3:
        momentum = 0.0
    else:
        ma3 = receita.rolling(3).mean().iloc[-1]
        ultimo = receita.iloc[-1]
        momentum = 0.0 if ma3 == 0 else (ultimo - ma3) / ma3

    # Erro relativo
    media = receita.mean()
    if media == 0 or rmse is None:
        erro_rel = 0.0
    else:
        erro_rel = rmse / media

    # --------------------------------------------------------------------------
    # NORMALIZAÇÃO
    # --------------------------------------------------------------------------

    score_growth = logistic_positive(growth, center=0.05, steepness=12)
    score_momentum = logistic_positive(momentum, center=0.05, steepness=12)
    score_vol = logistic_negative(vol, center=0.12, steepness=15)
    score_erro = logistic_negative(erro_rel, center=0.10, steepness=15)

    componentes = {
        "crescimento": round(float(score_growth), 2),
        "volatilidade": round(float(score_vol), 2),
        "momentum": round(float(score_momentum), 2),
        "erro_modelo": round(float(score_erro), 2)
    }

    # --------------------------------------------------------------------------
    # PESOS
    # --------------------------------------------------------------------------

    if pesos is not None:
        _validar_pesos(pesos)
    else:
        if preset not in PESOS_PRESETS:
            raise ValueError("Preset inválido.")
        pesos = PESOS_PRESETS[preset]

    # --------------------------------------------------------------------------
    # ÍNDICE FINAL
    # --------------------------------------------------------------------------

    indice = sum(componentes[k] * pesos[k] for k in componentes)

    # Clamp (garantia de domínio)
    indice = max(0.0, min(100.0, indice))

    indice = round(indice, 2)

    return {
        "indice": float(indice),
        "componentes": componentes
    }


# ==============================================================================
# CLASSIFICAÇÃO
# ==============================================================================

def classificar_saude(indice):

    if not isinstance(indice, (int, float)):
        raise ValueError("Índice inválido.")

    if indice < 0 or indice > 100:
        raise ValueError("Índice fora do intervalo esperado (0-100).")

    if indice < 40:
        return "Crítico"
    elif indice < 60:
        return "Instável"
    elif indice < 75:
        return "Saudável"
    else:
        return "Excelente"


# ==============================================================================
# RELATÓRIO AUTOMÁTICO
# ==============================================================================

def gerar_relatorio_saude(indice: float, classificacao: str, componentes: dict) -> str:

    if not isinstance(componentes, dict):
        raise ValueError("Componentes inválidos.")

    crescimento = componentes.get("crescimento", 0)
    volatilidade = componentes.get("volatilidade", 0)
    momentum = componentes.get("momentum", 0)
    erro_modelo = componentes.get("erro_modelo", 0)

    pontos_fortes = []
    pontos_fracos = []

    if crescimento >= 60:
        pontos_fortes.append("Crescimento consistente da receita")
    else:
        pontos_fracos.append("Crescimento abaixo do ideal")

    if volatilidade >= 60:
        pontos_fortes.append("Baixa volatilidade recente")
    else:
        pontos_fracos.append("Oscilação elevada nas receitas")

    if momentum >= 60:
        pontos_fortes.append("Momentum positivo no curto prazo")
    else:
        pontos_fracos.append("Perda de tração recente")

    if erro_modelo >= 60:
        pontos_fortes.append("Boa previsibilidade do modelo")
    else:
        pontos_fracos.append("Incerteza elevada nas previsões")

    relatorio = (
        f"Diagnóstico Financeiro\n\n"
        f"Índice Geral: {indice} ({classificacao})\n\n"
        f"Análise:\n\n"
        f"Pontos Fortes:\n"
        f"- " + ("\n- ".join(pontos_fortes) if pontos_fortes else "Nenhum destaque relevante.") + "\n\n"
        f"Pontos de Atenção:\n"
        f"- " + ("\n- ".join(pontos_fracos) if pontos_fracos else "Nenhum risco significativo identificado.") + "\n\n"
        f"Conclusão:\n"
        f"O cenário atual é classificado como '{classificacao}'. "
        f"Recomenda-se monitoramento contínuo dos componentes com menor pontuação "
        f"para fortalecimento estrutural da saúde financeira."
    )

    return relatorio