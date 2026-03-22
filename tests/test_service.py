def test_prediction_service():
    from src.services.prediction_service import predict

    data = [1000] * 12
    result = predict(data)

    assert result is not None
    