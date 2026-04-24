# reports.py


def gerar_relatorio(dados: dict) -> str:
    """
    Gera um relatório simples a partir de um dicionário de dados.
    Retorna uma string indicando o resultado ou erro.
    """
    if not isinstance(dados, dict):
        raise ValueError("Entrada deve ser um dicionário.")

    if not dados:
        return "Erro: dados ausentes"

    valores = dados.get("valores")
    if valores is None:
        return "Erro: dados inválidos"

    return "Relatório válido"


def generate_fluxo_caixa(data):
    """
    Gera relatório de fluxo de caixa a partir de um DataFrame.
    Retorna um dicionário com métricas financeiras.
    """
    required_cols = {"receitas", "despesas"}
    if not required_cols.issubset(data.columns):
        raise ValueError(f"DataFrame deve conter colunas {required_cols}")

    total_receitas = int(data["receitas"].sum())
    total_despesas = int(data["despesas"].sum())
    saldo_final = total_receitas - total_despesas
    saldo_medio = int((data["receitas"] - data["despesas"]).mean())

    return {
        "total_receitas": total_receitas,
        "total_despesas": total_despesas,
        "saldo_final": saldo_final,
        "saldo_medio": saldo_medio,
    }
