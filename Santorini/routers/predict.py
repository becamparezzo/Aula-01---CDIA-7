from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from model_utils import load_model

router = APIRouter()

model = load_model()

class ChurnInput(BaseModel):
    dias_sem_login: int = Field(..., ge=0, description="Dias desde o último login")
    num_chamados: int = Field(..., ge=0, description="Número de chamados abertos")
    valor_mensalidade: float = Field(..., gt=0, description="Valor da mensalidade em R$")
    meses_contrato: int = Field(..., ge=0, description="Meses de contrato ativo")
    nps_score: int = Field(..., ge=0, le=10, description="NPS score do cliente (0-10)")

class ChurnOutput(BaseModel):
    churn: bool
    probabilidade: float
    mensagem: str

@router.post("/", response_model=ChurnOutput)
async def predict_churn(dados: ChurnInput):
    try:
        features = [[
            dados.dias_sem_login,
            dados.num_chamados,
            dados.valor_mensalidade,
            dados.meses_contrato,
            dados.nps_score
        ]]

        predicao = model.predict(features)[0]
        probabilidade = model.predict_proba(features)[0][1]

        return ChurnOutput(
            churn=bool(predicao),
            probabilidade=round(float(probabilidade), 4),
            mensagem="Cliente com risco de churn" if predicao else "Cliente sem risco de churn"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))