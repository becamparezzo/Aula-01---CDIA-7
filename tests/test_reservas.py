from fastapi.testclient import TestClient
from Santorini.main import app
from datetime import datetime, timedelta

client = TestClient(app)

def data_futura(horas=2):
    return (datetime.now() + timedelta(hours=horas)).isoformat()

def test_criar_reserva():
    payload = {
        "mesa": 1,
        "nome": "Maria Silva",
        "pessoas": 4,
        "data_hora": data_futura(2)
    }
    response = client.post("/reservas/", json=payload)
    assert response.status_code == 200
    assert response.json()["mesa"] == 1
    assert response.json()["ativa"] == True

def test_criar_reserva_data_passada():
    payload = {
        "mesa": 2,
        "nome": "João Santos",
        "pessoas": 2,
        "data_hora": data_futura(0.1)
    }
    response = client.post("/reservas/", json=payload)
    assert response.status_code == 422

def test_criar_reserva_mesa_invalida():
    payload = {
        "mesa": 99,
        "nome": "Ana Costa",
        "pessoas": 2,
        "data_hora": data_futura(2)
    }
    response = client.post("/reservas/", json=payload)
    assert response.status_code == 422

def test_criar_reserva_pessoas_demais():
    payload = {
        "mesa": 3,
        "nome": "Grupo Grande",
        "pessoas": 15,
        "data_hora": data_futura(2)
    }
    response = client.post("/reservas/", json=payload)
    assert response.status_code == 422

def test_listar_reservas():
    response = client.get("/reservas/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_buscar_reserva_inexistente():
    response = client.get("/reservas/999")
    assert response.status_code == 404

def test_cancelar_reserva():
    payload = {
        "mesa": 5,
        "nome": "Carlos Lima",
        "pessoas": 3,
        "data_hora": data_futura(3)
    }
    response = client.post("/reservas/", json=payload)
    assert response.status_code == 200
    reserva_id = response.json()["id"]

    response = client.delete(f"/reservas/{reserva_id}")
    assert response.status_code == 200
    assert "cancelada" in response.json()["mensagem"]
