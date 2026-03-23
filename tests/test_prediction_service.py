def test_prediction_service_input_none_deve_falhar():
    from src.services.prediction_service import predict
    import pytest

    with pytest.raises(ValueError):
        predict([])
