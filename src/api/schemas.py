from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


# ==============================
# INPUT - Série temporal
# ==============================
class ReceitaInput(BaseModel):
    receita: List[float] = Field(
        ...,
        min_length=12,
        max_length=12,
        description="Receita mensal da empresa (últimos 12 meses)",
    )

    model_config = ConfigDict(
        extra="forbid",
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
        },
    )


# ==============================
# INPUT - API de scoring
# ==============================
class ScoreRequest(BaseModel):
    receita: float = Field(
        ...,
        gt=0,
        description="Receita deve ser maior que zero",
    )
    despesas: float = Field(
        ...,
        ge=0,
        description="Despesas não podem ser negativas",
    )
    divida: float = Field(
        ...,
        ge=0,
        description="Dívida não pode ser negativa",
    )

    model_config = ConfigDict(extra="forbid")


# ==============================
# OUTPUT - API de scoring
# ==============================
class ScoreResponse(BaseModel):
    score: float = Field(
        ...,
        ge=0,
        le=100,
        description="Score financeiro calculado (0 a 100)",
    )

    classificacao: Literal[
        "Saudável",
        "Estável",
        "Risco",
        "Crítico",
    ]

    recomendacao: str = Field(
        ...,
        min_length=10,
        description="Recomendação automática baseada no score",
    )

    model_config = ConfigDict(extra="forbid")


# ==============================
# INPUT - Diagnóstico
# ==============================
class DiagnosisRequest(BaseModel):
    receita: float = Field(..., gt=0)
    despesas: float = Field(..., ge=0)
    divida: float = Field(..., ge=0)
    reserva: float = Field(..., ge=0)

    model_config = ConfigDict(extra="forbid")

    @field_validator("despesas")
    @classmethod
    def expenses_not_greater_than_income(cls, v, values):
        receita = values.data.get("receita")
        if receita is not None and v > receita:
            raise ValueError("Despesas não podem ser maiores que a receita")
        return v


# ==============================
# OUTPUT - Diagnóstico
# ==============================
class DiagnosisResponse(BaseModel):
    score: int = Field(..., ge=0, le=100)

    classification: Literal[
        "Crítico",
        "Atenção",
        "Estável",
        "Saudável",
    ]

    diagnosis: str = Field(..., min_length=10)

    alerts: List[str] = Field(
        ...,
        min_length=3,
        max_length=3,
    )

    recommendations: List[str] = Field(
        ...,
        min_length=3,
        max_length=3,
    )

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "score": 74,
                "classification": "Estável",
                "diagnosis": (
                    "Sua saúde financeira apresenta estabilidade moderada, "
                    "mas exige atenção preventiva."
                ),
                "alerts": [
                    "Reserva abaixo do ideal",
                    "Comprometimento parcial da renda",
                    "Baixa margem para imprevistos",
                ],
                "recommendations": [
                    "Reduzir despesas variáveis em 8%",
                    "Construir reserva de emergência",
                    "Revisar gastos recorrentes",
                ],
            }
        },
    )