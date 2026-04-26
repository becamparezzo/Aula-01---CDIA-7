import pytest
from fastapi.testclient import TestClient
from Santorini.main import app

client = TestClient(app)

def test_predict_churn_positivo():
    payload = {
        "dias_sem_login": 90,
        "num_chamados": 8,
        "valor_mensalidade": 200.0,
        "meses_contrato": 3,
        "nps_score": 2
    }
    response = client.post("/predict/", json=payload)
    assert response.status_code == 200
    assert response.json()["churn"] == True
    assert "probabilidade" in response.json()
    assert "mensagem" in response.json()

def test_predict_churn_negativo():
    payload = {
        "dias_sem_login": 2,
        "num_chamados": 0,
        "valor_mensalidade": 300.0,
        "meses_contrato": 48,
        "nps_score": 9
    }
    response = client.post("/predict/", json=payload)
    assert response.status_code == 200
    assert response.json()["churn"] == False

def test_predict_campo_invalido():
    payload = {
        "dias_sem_login": -1,
        "num_chamados": 0,
        "valor_mensalidade": 300.0,
        "meses_contrato": 48,
        "nps_score": 9
    }
    response = client.post("/predict/", json=payload)
    assert response.status_code == 422

def test_predict_nps_fora_do_range():
    payload = {
        "dias_sem_login": 10,
        "num_chamados": 0,
        "valor_mensalidade": 300.0,
        "meses_contrato": 48,
        "nps_score": 15
    }
    response = client.post("/predict/", json=payload)
    assert response.status_code == 422
