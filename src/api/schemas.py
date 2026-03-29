from pydantic import BaseModel, Field, ConfigDict
from typing import List


# ==============================
# INPUT - Série temporal (mantido)
# ==============================
class ReceitaInput(BaseModel):
    receita: List[float] = Field(
        ...,
        min_length=12,
        max_length=12,
        description="Receita mensal da empresa (últimos 12 meses)",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "receita": [
                    10000,
                    12000,
                    11000,
                    13000,
                    12500,
                    14000,
                    15000,
                    14500,
                    16000,
                    17000,
                    16500,
                    18000,
                ]
            }
        }
    )


# ==============================
# INPUT - API de scoring
# ==============================
class ScoreRequest(BaseModel):
    receita: float = Field(..., gt=0, description="Receita deve ser maior que zero")
    despesas: float = Field(..., ge=0, description="Despesas não podem ser negativas")
    divida: float = Field(..., ge=0, description="Dívida não pode ser negativa")


# ==============================
# OUTPUT - API de scoring
# ==============================
class ScoreResponse(BaseModel):
    score: float = Field(..., description="Score financeiro calculado")
    classificacao: str = Field(..., description="Classificação do perfil financeiro")
    recomendacao: str = Field(
        ..., description="Recomendação automática baseada no score"
    )
