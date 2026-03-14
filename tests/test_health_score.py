from src.simulation.simulator import gerar_cenario
from src.core.health_score import calcular_indice_saude


def test_indice_esta_no_intervalo_valido():
    df = gerar_cenario(meses=36)

    resultado = calcular_indice_saude(df, rmse=500)

    assert 0 <= resultado["indice"] <= 100


def test_componentes_existem():
    df = gerar_cenario(meses=36)

    resultado = calcular_indice_saude(df, rmse=500)

    componentes = resultado["componentes"]

    assert "crescimento" in componentes
    assert "volatilidade" in componentes
    assert "momentum" in componentes
    assert "erro_modelo" in componentes


def test_classificacao_coerente():
    df = gerar_cenario(meses=36)

    resultado = calcular_indice_saude(df, rmse=500)

    indice = resultado["indice"]

    if indice < 40:
        esperado = "Crítico"
    elif indice < 60:
        esperado = "Instável"
    elif indice < 75:
        esperado = "Saudável"
    else:
        esperado = "Excelente"

    from src.core.health_score import classificar_saude

    assert classificar_saude(indice) == esperado


def test_indice_maior_em_cenario_de_crescimento():
    df_crescimento = gerar_cenario(
        meses=36,
        receita_inicial=20000,
        receita_final=50000,
        seed=42
    )

    df_queda = gerar_cenario(
        meses=36,
        receita_inicial=50000,
        receita_final=20000,
        seed=42
    
    )

    resultado_crescimento = calcular_indice_saude(df_crescimento, rmse=500)
    resultado_queda = calcular_indice_saude(df_queda, rmse=500)

    assert resultado_crescimento["indice"] > resultado_queda["indice"]


def test_indice_cai_com_choque_negativo():
    df_base = gerar_cenario(
        meses=36,
        receita_inicial=20000,
        receita_final=40000,
        choque_em=None,seed=42
    
    )

    df_choque = gerar_cenario(
        meses=36,
        receita_inicial=20000,
        receita_final=40000,
        choque_em=18,
        intensidade_choque=-0.4,
        seed=42
    
    
    )

    resultado_base = calcular_indice_saude(df_base, rmse=500)
    resultado_choque = calcular_indice_saude(df_choque, rmse=500)

    assert resultado_choque["indice"] < resultado_base["indice"]

def test_regressao_deterministica_indice():
    df_1 = gerar_cenario(
        meses=36,
        receita_inicial=25000,
        receita_final=45000,
        volatilidade=3000,
        seed=123
    )

    df_2 = gerar_cenario(
        meses=36,
        receita_inicial=25000,
        receita_final=45000,
        volatilidade=3000,
        seed=123
    )

    resultado_1 = calcular_indice_saude(df_1, rmse=500)
    resultado_2 = calcular_indice_saude(df_2, rmse=500)

    assert resultado_1 == resultado_2

