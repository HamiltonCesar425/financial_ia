import time
from fastapi import FastAPI, APIRouter, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.middleware.cors import CORSMiddleware

import src.core.health_score as health_score

from src.api.schemas import ScoreResponse, ScoreRequest
from src.api.metrics import update_metrics
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
# App + Router
# ======================================
app = FastAPI(title="Financial AI")
router = APIRouter(prefix="", tags=["Financial AI"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "https://financial-ia-sandy.vercel.app",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app)

# ======================================
# Alias para testes
# ======================================
calcular_indice_saude_input_simples = health_score.calcular_indice_saude_input_simples


# ======================================
# Endpoints auxiliares
# ======================================
@router.get("/", summary="Root")
def root():
    return {"message": "Diagnostico Financeiro Automatizado API online"}


@router.get("/health", summary="Health Check")
def health_check():
    return {"status": "ok"}


# ======================================
# Endpoint simples (ajustado)
# ======================================
@router.post("/calcular", summary="Cálculo simples")
def calcular_endpoint(payload: dict):
    if "receita" not in payload or "despesas" not in payload:
        raise HTTPException(status_code=422, detail="Missing fields")

    try:
        resultado = payload["receita"] - payload["despesas"]
        return {"resultado": resultado}
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid data")


# ======================================
# Classificação
# ======================================
def _classificar(score: float) -> str:
    if score >= 80:
        return "Saudável"
    elif score >= 60:
        return "Estável"
    elif score >= 40:
        return "Risco"
    return "Crítico"


def _gerar_recomendacao(score: float) -> str:
    if score >= 80:
        return "Mantenha o padrão financeiro atual."
    elif score >= 60:
        return "Atenção aos gastos variáveis."
    elif score >= 40:
        return "Reduza despesas e priorize quitação de dívidas."
    return "Risco elevado: reestruture sua vida financeira imediatamente."


# ======================================
# Endpoint principal
# ======================================
@router.post(
    "/score",
    response_model=ScoreResponse,
    summary="Cálculo de Score Financeiro",
)
def calcular_score(payload: ScoreRequest) -> ScoreResponse:
    start_time = time.time()

    try:
        result = calcular_indice_saude_input_simples(
            receita=payload.receita,
            despesas=payload.despesas,
            divida=payload.divida,
        )

        score = result["score"]
        classificacao = _classificar(score)
        recomendacao = _gerar_recomendacao(score)

        # Atualização centralizada de métricas
        update_metrics(
            receita=payload.receita,
            despesas=payload.despesas,
            divida=payload.divida,
            classificacao=classificacao.lower(),
            recomendacao=recomendacao.lower(),
        )

        prediction_count.inc()
        model_state_counter.labels(state="success").inc()

        return ScoreResponse(
            score=score,
            classificacao=classificacao,
            recomendacao=recomendacao,
        )

    except Exception as exc:
        logger.exception("Erro interno na predição")
        prediction_errors.inc()
        model_state_counter.labels(state="error").inc()
        raise HTTPException(
            status_code=500,
            detail="Erro interno na predição",
        ) from exc

    finally:
        elapsed = time.time() - start_time
        logger.info("Tempo de execução: %.4fs", elapsed)


# ======================================
# Router
# ======================================
app.include_router(router)
