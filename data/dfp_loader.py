import pandas as pd
from pathlib import Path


class DFPLoader:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)

    def _load_csv(self, filename: str) -> pd.DataFrame:
        file_path = self.base_path / filename
        df = pd.read_csv(file_path, sep=";", encoding="latin1")
        return df

    def _filter_company(self, df: pd.DataFrame, ticker: str) -> pd.DataFrame:
        return df[df["CD_CVM"].notna() & df["DENOM_CIA"].str.contains(ticker, case=False, na=False)]

    def get_balance_sheet(self, company_name: str, year: int) -> dict:
        """
        Retorna os principais dados do Balanço Consolidado.
        """

        ativo_file = f"dfp_cia_aberta_BPA_con_{year}.csv"
        passivo_file = f"dfp_cia_aberta_BPP_con_{year}.csv"

        df_ativo = self._load_csv(ativo_file)
        df_passivo = self._load_csv(passivo_file)

        df_ativo = self._filter_company(df_ativo, company_name)
        df_passivo = self._filter_company(df_passivo, company_name)

        # Última data do exercício
        df_ativo = df_ativo[df_ativo["DT_REFER"] == f"{year}-12-31"]
        df_passivo = df_passivo[df_passivo["DT_REFER"] == f"{year}-12-31"]

        result = {}

        # ATIVO
        result["ativo_total"] = df_ativo.loc[
            df_ativo["DS_CONTA"] == "Ativo Total", "VL_CONTA"
        ].astype(float).sum()

        result["ativo_circulante"] = df_ativo.loc[
            df_ativo["DS_CONTA"] == "Ativo Circulante", "VL_CONTA"
        ].astype(float).sum()

        result["caixa"] = df_ativo.loc[
            df_ativo["DS_CONTA"].str.contains("Caixa", case=False, na=False),
            "VL_CONTA",
        ].astype(float).sum()

        # PASSIVO
        result["passivo_total"] = df_passivo.loc[
            df_passivo["DS_CONTA"] == "Passivo Total", "VL_CONTA"
        ].astype(float).sum()

        result["passivo_circulante"] = df_passivo.loc[
            df_passivo["DS_CONTA"] == "Passivo Circulante", "VL_CONTA"
        ].astype(float).sum()

        result["patrimonio_liquido"] = df_passivo.loc[
            df_passivo["DS_CONTA"] == "Patrimônio Líquido", "VL_CONTA"
        ].astype(float).sum()

        return result


if __name__ == "__main__":
    loader = DFPLoader(base_path="data/dfp_cia_aberta_2018")
    balance = loader.get_balance_sheet("Ambev", 2018)
    print(balance)