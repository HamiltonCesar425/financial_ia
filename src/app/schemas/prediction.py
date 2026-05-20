from typing import Dict, List

from pydantic import BaseModel


class PredictionResponse(BaseModel):
    current_score: int
    projected_score_30d: int
    delta: int
    trend: str
    confidence: float
    confidence_formula: str
    confidence_factors: Dict[str, float]
    projection_horizon_days: int
    prediction_context: str
    explanatory_factors: List[str]
