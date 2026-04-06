import time
from fastapi import FastAPI, APIRouter, Response, HTTPException, Request
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import generate_latest

# Importa métricas customizadas
from src.api.metrics import (
    receita_metric,
    despesas_metric,
    divida_metric,
    classificacao_metric,
    recomendacao_metric,
)

# Importa módulo de cálculo
import src.core.health_score as health_score

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
router = APIRouter(prefix="", tags=["Financial IA"])

Instrumentator().instrument(app).expose(app)

# ======================================
# Expor função para facilitar monkeypatch nos testes
# ======================================
calcular_indice_saude_input_simples = health_score.calcular_indice_saude_input_simples


# ======================================
# Endpoints auxiliares
# ======================================
@router.get("/health", summary="Health Check")
def health_check():
    return {"status": "ok"}


@router.get("/metrics", summary="Prometheus Metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")


@router.post("/calcular", summary="Cálculo simples de receitas - despesas")
async def calcular_endpoint(request: Request):
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    if not data or "dados" not in data:
        raise HTTPException(status_code=400, detail="Invalid request")

    if "receitas" not in data or "despesas" not in data:
        raise HTTPException(status_code=422, detail="Missing fields")

    resultado = data["receitas"] - data.get("despesas", 0)
    return {"resultado": resultado}


# ======================================
# Lógica de classificação
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
    "/score", response_model=ScoreResponse, summary="Cálculo de Score Financeiro"
)
def calcular_score(payload: ScoreRequest) -> ScoreResponse:
    start_time = time.time()

    try:
        receita_metric.set(payload.receita)
        despesas_metric.set(payload.despesas)
        divida_metric.set(payload.divida)

        score = calcular_indice_saude_input_simples(
            receita=payload.receita,
            despesas=payload.despesas,
            divida=payload.divida,
        )

        classificacao = _classificar(score)
        recomendacao = _gerar_recomendacao(score)

        classificacao_map = {"Saudável": 1, "Estável": 2, "Risco": 3, "Crítico": 4}
        classificacao_metric.set(classificacao_map[classificacao])
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
