def test_payload_sem_data_e_sem_campos_deve_falhar(client):
    response = client.post("/score", json={})

    assert response.status_code == 422


def test_payload_vazio_retorna_422(client):
    response = client.post("/score", json={})
    assert response.status_code == 422


def test_payload_com_campos_invalidos(client):
    response = client.post(
        "/score", json={"receita": -1000, "despesas": -500, "divida": -200}
    )
    assert response.status_code == 422


def test_payload_com_valores_none(client):
    response = client.post(
        "/score", json={"receita": None, "despesas": None, "divida": None}
    )
    assert response.status_code == 422
