from fastapi.testclient import TestClient
from Santorini.main import app

client = TestClient(app)

def test_listar_pratos():
    response = client.get("/pratos/pratos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_buscar_prato_existente():
    response = client.get("/pratos/pratos/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_buscar_prato_inexistente():
    response = client.get("/pratos/pratos/999")
    assert response.status_code == 404

def test_adicionar_prato():
    novo = {
        "nome": "Lasanha",
        "categoria": "Prato Principal",
        "preco": 55.00,
        "disponivel": True
    }
    response = client.post("/pratos/pratos", json=novo)
    assert response.status_code == 200
    assert response.json()["nome"] == "Lasanha"

def test_prato_nome_curto():
    invalido = {
        "nome": "Ab",
        "categoria": "Prato Principal",
        "preco": 55.00
    }
    response = client.post("/pratos/pratos", json=invalido)
    assert response.status_code == 422
