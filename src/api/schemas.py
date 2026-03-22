from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Any


class ReceitaInput(BaseModel):
    receita: List[float] = Field(
        ...,
        min_length=12,
        max_length=12,
        description="Receita mensal da empresa (últimos 12 meses)"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "receita": [
                    10000, 12000, 11000, 13000,
                    12500, 14000, 15000, 14500,
                    16000, 17000, 16500, 18000
                ]
            }
        }
    )


class ScoreResponse(BaseModel):
    score: float = Field(
        ...,
        ge=0,
        le=100,
        description="Score financeiro da empresa (0 a 100)"
    )
    classification: str = Field(
        ...,
        description="Classificação do risco financeiro"
    )
    pillars: Dict[str, float] = Field(
        ...,
        description="Indicadores que compõem o score"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Informações adicionais do processamento"
    )
    