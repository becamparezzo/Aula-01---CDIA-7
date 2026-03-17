from fastapi import APIRouter, HTTPException
from typing import Optional
from datetime import datetime
from ..models import PratoInput, PratoOutput, DisponibilidadeInput

router = APIRouter()

pratos = [
    # Entradas
    {"id": 1, "nome": "Brusqueta", "categoria": "Entrada", "preco": 34.00, "disponivel": True},
    {"id": 2, "nome": "Táboa de antepastos (Acompanha pão de fermentação natural)", "categoria": "Entrada", "preco": 40, "disponivel": True},
    {"id": 3, "nome": "Pupunha gratinado com isca de polvo salteado", "categoria": "Entrada", "preco": 52, "disponivel": True},

    # Pratos Principais
    {"id": 4, "nome": "Risoto de frutos do mar", "categoria": "Prato Principal", "preco": 69.90, "disponivel": True},
    {"id": 5, "nome": "Arroz negro com polvo", "categoria": "Prato Principal", "preco": 72.00, "disponivel": False},
    {"id": 6, "nome": "Salada grega com Crab Cakes", "categoria": "Prato Principal", "preco": 60.00, "disponivel": True},
    {"id": 7, "nome": "Cuscuz Marroquino com peixe branco assado", "categoria": "Prato Principal", "preco": 65.00, "disponivel": True},
    {"id": 8, "nome": "Paella", "categoria": "Prato Principal", "preco": 70.00, "disponivel": False},

    # Sobremesas
    {"id": 9, "nome": "Baklava", "categoria": "Sobremesa", "preco": 39.00, "disponivel": True},
    {"id": 10, "nome": "Panna Cotta", "categoria": "Sobremesa", "preco": 27.00, "disponivel": True},
    {"id": 11, "nome": "Tiramissu", "categoria": "Sobremesa", "preco": 32.00, "disponivel": True}
]

@router.get("/pratos")
async def listar_pratos(categoria: Optional[str] = None,
                        preco_max: Optional[float] = None,
                        apenas_disponiveis: bool = False):

    resultado = pratos

    if categoria:
        resultado = [p for p in resultado if p["categoria"] == categoria]
    if preco_max:
        resultado = [p for p in resultado if p["preco"] <= preco_max]
    if apenas_disponiveis:
        resultado = [p for p in resultado if p["disponivel"]]
    return resultado

@router.get("/pratos/{prato_id}")
async def buscar_prato(prato_id: int):
    for prato in pratos:
        if prato["id"] == prato_id:
            return prato
    raise HTTPException(
        status_code=404,
        detail=f"Prato com id {prato_id} não encontrado"
    )

@router.get("/pratos/{prato_id}/detalhes")
async def buscar_detalhes_prato(prato_id: int, formato: str = "completo"):
    for prato in pratos:
        if prato["id"] == prato_id:
            if formato == "resumido":
                return {"nome": prato["nome"], "preco": prato["preco"]}
            return prato
    raise HTTPException(status_code=404, detail="Prato não encontrado")



@router.post("/pratos", response_model=PratoOutput)
async def adicionar_prato(prato: PratoInput):
    novo_id = max(p["id"] for p in pratos) + 1
    novo_prato = {
        "id": novo_id, 
        "criado_em": datetime.now().isoformat(),
        **prato.model_dump()
    }
    pratos.append(novo_prato)
    return novo_prato


@router.post("/pratos/{prato_id}/disponibilidade")
async def atualizar_disponibilidade(prato_id: int, body: DisponibilidadeInput):
    # Erro 404: recurso não existe
    prato = next((p for p in pratos if p["id"] == prato_id), None)
    if not prato:
        raise HTTPException(status_code=404, detail="Prato não encontrado")

    prato["disponivel"] = body.disponivel
    return prato