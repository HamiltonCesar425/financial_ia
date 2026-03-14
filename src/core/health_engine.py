from src.core.health_score import calcular_indice_saude


class HealthScoreEngine:

    def __init__(self, preset="balanceado"):
        self.preset = preset

    def compute(self, df):

        # RMSE fixo provisório para backtest
        # (depois podemos tornar dinâmico)
        resultado = calcular_indice_saude(
            df,
            rmse=500,
            preset=self.preset
        )

        return resultado["indice"]