from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional

class PratoInput(BaseModel):
    nome: str = Field(min_length=3, max_length=100, description="Nome do prato")
    categoria: str = Field(pattern="^(Entrada|Prato Principal|Sobremesa)$")
    preco: float = Field(gt=0, description="Preço em reais")
    descricao: Optional[str] = Field(default=None, max_length=500)
    disponivel: bool = True
    preco_promocional: Optional[float] = Field(default=None, gt=0, description="Preço promocional em reais")

    @model_validator(mode="after")
    def validar_preco_promocional(self):
        if self.preco_promocional is not None:
            if self.preco_promocional >= self.preco:
                raise ValueError("O preço promocional deve ser menor que o preço original")
            desconto = self.preco - self.preco_promocional
            if desconto / self.preco > 0.5:
                raise ValueError("O desconto promocional não pode ser maior que 50% do preço original")
        return self

class PratoOutput(PratoInput):
    id: int
    criado_em: str

class DisponibilidadeInput(BaseModel):
    disponivel: bool = Field(description="Indica se o prato está disponível para pedido")
