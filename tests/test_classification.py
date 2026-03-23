from src.engine.classification import classificar

def test_classification_boundaries():
    assert classificar(95) == "Excelente"
    assert classificar(80) == "Bom"
    assert classificar(60) == "Regular"
    assert classificar(30) == "Crítico"
    