import pytest


def test_predict_erro_interno(monkeypatch):
    from src.services import prediction_service

    def mock_predict(*args, **kwargs):
        raise Exception("falha interna")

    monkeypatch.setattr(
        prediction_service.engine,
        "predict",
        mock_predict
    )

    with pytest.raises(Exception):
        prediction_service.predict([1000] * 12)


def test_predict_input_invalido():
    from src.services import prediction_service

    with pytest.raises(ValueError):
        prediction_service.predict(None)

def test_predict_sucesso(monkeypatch):
    from src.services import prediction_service

    def mock_predict(*args, **kwargs):
        return {"score": 85}

    monkeypatch.setattr(
        prediction_service.engine,
        "predict",
        mock_predict
    )

    result = prediction_service.predict([1000] * 12)

    assert result["score"] == 85
    