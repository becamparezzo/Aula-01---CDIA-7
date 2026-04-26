from fastapi.testclient import TestClient
from Santorini.main import app

client = TestClient(app)

def test_listar_bebidas():
    response = client.get("/bebidas/bebidas")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_listar_bebidas_por_tipo():
    response = client.get("/bebidas/bebidas?tipo=Suco")
    assert response.status_code == 200
    for b in response.json():
        assert b["tipo"] == "Suco"

def test_listar_bebidas_nao_alcoolicas():
    response = client.get("/bebidas/bebidas?alcoolica=false")
    assert response.status_code == 200
    for b in response.json():
        assert b["alcoolica"] == False

def test_buscar_bebida_existente():
    response = client.get("/bebidas/bebidas/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_buscar_bebida_inexistente():
    response = client.get("/bebidas/bebidas/999")
    assert response.status_code == 404

def test_adicionar_bebida():
    nova = {
        "nome": "Limonada",
        "tipo": "Suco",
        "alcoolica": False,
        "preco": 14.00,
        "volume_ml": 300
    }
    response = client.post("/bebidas/bebidas", json=nova)
    assert response.status_code == 200
    assert response.json()["nome"] == "Limonada"

def test_bebida_tipo_invalido():
    invalida = {
        "nome": "Groselha",
        "tipo": "Xarope",
        "alcoolica": False,
        "preco": 10.00,
        "volume_ml": 300
    }
    response = client.post("/bebidas/bebidas", json=invalida)
    assert response.status_code == 422
