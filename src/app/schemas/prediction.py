from typing import List

from pydantic import BaseModel


class PredictionResponse(BaseModel):
    current_score: int
    projected_score_30d: int
    delta: int
    trend: str
    confidence: float
    projection_horizon_days: int
    explanatory_factors: List[str]
