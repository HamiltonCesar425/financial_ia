import time
import os

from pydantic import BaseModel
from fastapi import FastAPI, APIRouter, Response, HTTPException

from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import generate_latest

# Importa métricas customizadas
from .metrics import (  # noqa: F401
    receita_metric,
    despesas_metric,
    divida_metric,
    classificacao_metric,
    recomendacao_metric,
)

from src.core.health_score import calcular_indice_saude_input_simples
from src.api.schemas import ScoreResponse, ScoreRequest
from src.core.logging import setup_logging
from src.observability.metrics import (
    prediction_count,
    prediction_errors,
    model_state_counter,
)

# ======================================
# Logging
# ======================================
logger = setup_logging()
logger.info("Router de API inicializado")

# ======================================
# App + Router Initialization
# ======================================
app = FastAPI(title="Financial AI")
router = APIRouter(
    prefix="", tags=["Financial IA"]
)  # pode usar "/api" se quiser agrupar

# Expor métricas padrão do FastAPI
Instrumentator().instrument(app).expose(app)


# ======================================
# Endpoints auxiliares
# ======================================
@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")


# ======================================
# Lógica de classificação
# ======================================
def _classificar(score: float) -> str:
    if score >= 80:
        return "Saudável"
    if score >= 60:
        return "Estável"
    if score >= 40:
        return "Risco"
    return "Crítico"


def _gerar_recomendacao(score: float) -> str:
    if score >= 80:
        return "Mantenha o padrão financeiro atual."
    if score >= 60:
        return "Atenção aos gastos variáveis."
    if score >= 40:
        return "Reduza despesas e priorize quitação de dívidas."
    return "Risco elevado: reestruture sua vida financeira imediatamente."


# ======================================
# Endpoint principal
# ======================================
@router.post("/score", response_model=ScoreResponse)
def calcular_score(payload: ScoreRequest) -> ScoreResponse:
    start_time = time.time()

    try:
        # Atualiza métricas customizadas
        receita_metric.set(payload.receita)
        despesas_metric.set(payload.despesas)
        divida_metric.set(payload.divida)

        # Lógica de cálculo
        score = calcular_indice_saude_input_simples(
            receita=payload.receita,
            despesas=payload.despesas,
            divida=payload.divida,
        )

        classificacao = _classificar(score)
        recomendacao = _gerar_recomendacao(score)

        # Atualiza métricas de classificação e recomendação
        classificacao_map = {"Saudável": 1, "Estável": 2, "Risco": 3, "Crítico": 4}
        classificacao_metric.set(classificacao_map[classificacao])

        # PAra recomendação, usar um hash simples para diferenciar
        recomendacao_metric.set(abs(hash(recomendacao)) % 1000)

        prediction_count.inc()
        model_state_counter.labels(state="success").inc()

        return ScoreResponse(
            score=float(round(score, 2)),
            classificacao=classificacao,
            recomendacao=recomendacao,
        )

    except Exception as exc:
        logger.exception("Erro interno na predição")
        prediction_errors.inc()
        model_state_counter.labels(state="error").inc()
        raise HTTPException(status_code=500, detail="Erro interno na predição") from exc

    finally:
        elapsed = time.time() - start_time
        logger.info("Tempo de execução: %.4fs", elapsed)


# ======================================
# Inclui router no app
# ======================================
app.include_router(router)
