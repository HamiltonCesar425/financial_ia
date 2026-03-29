import numpy as np
import pandas as pd
from typing import Dict, Optional


# ==============================================================================
# PRESETS
# ==============================================================================

PESOS_PRESETS: Dict[str, Dict[str, float]] = {
    "balanceado": {
        "crescimento": 0.4,
        "volatilidade": 0.2,
        "momentum": 0.2,
        "erro_modelo": 0.2,
    },
    "conservador": {
        "crescimento": 0.25,
        "volatilidade": 0.35,
        "momentum": 0.15,
        "erro_modelo": 0.25,
    },
    "agressivo": {
        "crescimento": 0.45,
        "volatilidade": 0.15,
        "momentum": 0.20,
        "erro_modelo": 0.20,
    },
}


# ==============================================================================
# FUNÇÕES DE NORMALIZAÇÃO
# ==============================================================================

def _safe_exp(x: float) -> float:
    return np.exp(np.clip(x, -500, 500))


def logistic_positive(x: float, center: float = 0.05, steepness: float = 12) -> float:
    x = np.nan_to_num(x, nan=0.0, posinf=1e6, neginf=-1e6)
    return 100 / (1 + _safe_exp(-steepness * (x - center)))


def logistic_negative(x: float, center: float = 0.10, steepness: float = 12) -> float:
    x = np.nan_to_num(x, nan=0.0, posinf=1e6, neginf=-1e6)
    return 100 / (1 + _safe_exp(steepness * (x - center)))


# ==============================================================================
# VALIDAÇÕES
# ==============================================================================

def _validar_dataframe(df: pd.DataFrame) -> None:
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Entrada deve ser um DataFrame.")

    if df.empty:
        raise ValueError("DataFrame não pode ser vazio.")

    if "receita" not in df.columns:
        raise ValueError("Coluna 'receita' obrigatória.")


def _validar_rmse(rmse: Optional[float]) -> None:
    if rmse is None:
        return

    if not isinstance(rmse, (int, float)):
        raise ValueError("RMSE deve ser numérico.")

    if np.isnan(rmse) or np.isinf(rmse):
        raise ValueError("RMSE inválido.")

    if rmse < 0:
        raise ValueError("RMSE não pode ser negativo.")


def _validar_pesos(pesos: Dict[str, float]) -> None:
    if not isinstance(pesos, dict):
        raise ValueError("Pesos devem ser um dicionário.")

    if not np.isclose(sum(pesos.values()), 1.0):
        raise ValueError("A soma dos pesos deve ser 1.")

    for k in ["crescimento", "volatilidade", "momentum", "erro_modelo"]:
        if k not in pesos:
            raise ValueError(f"Peso ausente: {k}")


# ==============================================================================
# CORE PURO (SÉRIES)
# ==============================================================================

def calcular_indice_saude_series(
    receita: np.ndarray,
    rmse: Optional[float] = None,
    preset: str = "balanceado",
    pesos: Optional[Dict[str, float]] = None,
) -> Dict:

    if len(receita) == 0:
        raise ValueError("Série de receita vazia.")

    receita = receita.astype(float)

    # =========================
    # SANITIZAÇÃO GLOBAL
    # =========================
    receita = np.nan_to_num(receita, nan=0.0, posinf=1e6, neginf=-1e6)

    # =========================
    # MÉTRICAS
    # =========================

    # Crescimento (CAGR simplificado)
    if len(receita) < 2:
        growth = 0.0
    else:
        vi, vf = receita[0], receita[-1]
        n = len(receita) - 1
        growth = 0.0 if (vi <= 0 or vf <= 0) else (vf / vi) ** (1 / n) - 1

    # Variação percentual (robusta)
    if len(receita) > 1:
        denominator = receita[:-1]
        denominator = np.where(denominator == 0, 1e-8, denominator)

        pct = np.diff(receita) / denominator
        pct = np.nan_to_num(pct, nan=0.0, posinf=0.0, neginf=0.0)

        vol = np.std(pct[-6:]) if len(pct) > 0 else 0.0
    else:
        vol = 0.0

    # Momentum
    if len(receita) < 3:
        momentum = 0.0
    else:
        ma3 = np.mean(receita[-3:])
        momentum = 0.0 if abs(ma3) < 1e-8 else (receita[-1] - ma3) / ma3

    # Erro relativo
    media = np.mean(receita)
    media = media if abs(media) > 1e-8 else 1e-8

    erro_rel = 0.0 if rmse is None else rmse / media
    erro_rel = float(np.clip(erro_rel, 0.0, 1e6))

    # =========================
    # NORMALIZAÇÃO
    # =========================

    componentes = {
        "crescimento": float(logistic_positive(growth)),
        "volatilidade": float(logistic_negative(vol, center=0.12, steepness=15)),
        "momentum": float(logistic_positive(momentum)),
        "erro_modelo": float(logistic_negative(erro_rel, steepness=15)),
    }

    # =========================
    # PESOS
    # =========================

    if pesos:
        _validar_pesos(pesos)
    else:
        if preset not in PESOS_PRESETS:
            raise ValueError("Preset inválido.")
        pesos = PESOS_PRESETS[preset]

    # =========================
    # SCORE FINAL
    # =========================

    indice = sum(componentes[k] * pesos[k] for k in componentes)
    indice = float(np.clip(indice, 0.0, 100.0))

    return {
        "indice": round(indice, 2),
        "componentes": {k: round(v, 2) for k, v in componentes.items()},
    }


# ==============================================================================
# WRAPPER DATAFRAME
# ==============================================================================

def calcular_indice_saude(
    df: pd.DataFrame,
    rmse: Optional[float] = None,
    preset: str = "balanceado",
    pesos: Optional[Dict[str, float]] = None,
) -> Dict:

    _validar_dataframe(df)
    _validar_rmse(rmse)

    return calcular_indice_saude_series(
        receita=df["receita"].values,
        rmse=rmse,
        preset=preset,
        pesos=pesos,
    )


# ==============================================================================
# FUNÇÃO SIMPLES (API)
# ==============================================================================

def calcular_indice_saude_input_simples(
    receita: float,
    despesas: float,
    divida: float
) -> float:

    if receita <= 0:
        raise ValueError("Renda deve ser maior que zero.")

    if despesas < 0 or divida < 0:
        raise ValueError("Valores não podem ser negativos.")

    comprometimento = (despesas + divida) / receita
    score = 100 * (1 - comprometimento)

    return float(np.clip(score, 0.0, 100.0))


# ==============================================================================
# CLASSIFICAÇÃO
# ==============================================================================

def classificar_saude(indice: float) -> str:
    if not isinstance(indice, (int, float)):
        raise ValueError("Índice inválido.")

    if not (0 <= indice <= 100):
        raise ValueError("Índice fora do intervalo (0-100).")

    if indice < 40:
        return "Crítico"
    elif indice < 60:
        return "Instável"
    elif indice < 75:
        return "Saudável"
    return "Excelente"


# ==============================================================================
# RELATÓRIO
# ==============================================================================

def gerar_relatorio_saude(
    indice: float,
    classificacao: str,
    componentes: Dict[str, float],
) -> str:

    if not isinstance(componentes, dict):
        raise ValueError("Componentes inválidos.")

    relatorio = "Diagnóstico Financeiro\n\n"
    relatorio += f"Índice: {indice} ({classificacao})\n\n"

    return relatorio
