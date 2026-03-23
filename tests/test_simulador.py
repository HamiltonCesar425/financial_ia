def test_simulador_reprodutibilidade():
    from src.simulation.simulator import gerar_cenario

    df1 = gerar_cenario(seed=42)
    df2 = gerar_cenario(seed=42)

    assert df1.equals(df2)
