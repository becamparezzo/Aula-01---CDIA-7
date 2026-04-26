from fastapi.testclient import TestClient
from Santorini.main import app

client = TestClient(app)

def test_criar_pedido():
    payload = {
        "prato_id": 1,
        "quantidade": 2,
        "observacao": "Sem cebola"
    }
    response = client.post("/pedidos/pedidos", json=payload)
    assert response.status_code == 200
    assert response.json()["prato_id"] == 1
    assert response.json()["quantidade"] == 2
    assert "valor_total" in response.json()

def test_criar_pedido_prato_inexistente():
    payload = {
        "prato_id": 999,
        "quantidade": 1
    }
    response = client.post("/pedidos/pedidos", json=payload)
    assert response.status_code == 404

def test_criar_pedido_quantidade_invalida():
    payload = {
        "prato_id": 1,
        "quantidade": 0
    }
    response = client.post("/pedidos/pedidos", json=payload)
    assert response.status_code == 422

def test_criar_pedido_sem_observacao():
    payload = {
        "prato_id": 1,
        "quantidade": 1
    }
    response = client.post("/pedidos/pedidos", json=payload)
    assert response.status_code == 200
    assert response.json()["observacao"] is None
