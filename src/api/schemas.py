from pydantic import BaseModel, Field
from typing import List

class ReceitaInput(BaseModel):
    receita: List[float]= Field(
        ...,
        min_items=12,
        description="Receita mensal da empresa"
    )

class ScoreResponse(BaseModel):
    score: float
    classification: str
    pillars: dict
    metadata: dict    