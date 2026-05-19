from __future__ import annotations

from datetime import datetime
from statistics import mean
from typing import Any

MIN_HISTORY_SIZE = 2
TREND_DELTA_THRESHOLD = 20
HIGH_VOLATILITY_THRESHOLD = 45
ABRUPT_CHANGE_THRESHOLD = 60


def generate_insights(history: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Generates contextual insights from a user's historical financial scores.

    Expected history item shape:
    {
        "score": 720,
        "created_at": "2026-05-16T10:00:00"
    }
    """
    entries = _normalize_history(history)

    if len(entries) < MIN_HISTORY_SIZE:
        return {
            "status": "estavel",
            "trend": "ESTAVEL",
            "volatility": "unknown",
            "change_speed": "unknown",
            "delta": 0,
            "message": "Ainda nao ha historico suficiente para interpretar sua evolucao financeira.",
        }

    scores = [entry["score"] for entry in entries]
    delta = scores[-1] - scores[0]
    score_changes = _score_changes(scores)

    trend = _classify_trend(delta)
    status = _classify_status(trend)
    volatility = _classify_volatility(score_changes)
    change_speed = _classify_change_speed(score_changes)
    pattern = _classify_pattern(trend, volatility)

    return {
        "status": status,
        "trend": trend,
        "volatility": volatility,
        "change_speed": change_speed,
        "pattern": pattern,
        "delta": delta,
        "first_score": scores[0],
        "last_score": scores[-1],
        "analyses_count": len(scores),
        "message": _build_message(pattern, trend, volatility, change_speed),
    }


def _normalize_history(history: list[dict[str, Any]]) -> list[dict[str, Any]]:
    entries = []

    for item in history:
        score = item.get("score")

        if score is None:
            continue

        try:
            normalized_score = float(score)
        except (TypeError, ValueError):
            continue

        entries.append(
            {
                "score": normalized_score,
                "created_at": _parse_date(
                    item.get("created_at") or item.get("timestamp") or item.get("date")
                ),
            }
        )

    return sorted(
        entries,
        key=lambda entry: (
            entry["created_at"].timestamp()
            if entry["created_at"] is not None
            else float("-inf")
        ),
    )


def _parse_date(value: Any) -> datetime | None:
    if isinstance(value, datetime):
        return value

    if not isinstance(value, str) or not value:
        return None

    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _score_changes(scores: list[float]) -> list[float]:
    return [current - previous for previous, current in zip(scores, scores[1:])]


def _classify_trend(delta: float) -> str:
    if delta >= 20:
        return "ASCENDENTE"

    if delta <= -40:
        return "CRITICA"

    if delta <= -20:
        return "DESCENDENTE"

    return "ESTAVEL"


def _classify_status(trend: str) -> str:
    mapping = {
        "ASCENDENTE": "melhora",
        "ESTAVEL": "estavel",
        "DESCENDENTE": "queda",
        "CRITICA": "critico",
    }

    return mapping[trend]


def _classify_volatility(score_changes: list[float]) -> str:
    if not score_changes:
        return "unknown"

    average_change = mean(abs(change) for change in score_changes)

    if average_change >= HIGH_VOLATILITY_THRESHOLD:
        return "high"

    return "low"


def _classify_change_speed(score_changes: list[float]) -> str:
    if not score_changes:
        return "unknown"

    largest_change = max(abs(change) for change in score_changes)

    if largest_change >= ABRUPT_CHANGE_THRESHOLD:
        return "abrupt"

    return "gradual"


def _classify_pattern(trend: str, volatility: str) -> str:
    if volatility == "high":
        return "high_oscillation"

    if trend == "ASCENDENTE":
        return "consistent_improvement"

    if trend == {"DESCENDENTE", "CRITICA"}:
        return "consistent_decline"

    return "stability"


def _build_message(
    pattern: str,
    trend: str,
    volatility: str,
    change_speed: str,
) -> str:
    if pattern == "consistent_improvement":
        if change_speed == "abrupt":
            return "Seu score apresentou melhora acelerada " "nas últimas análises."

        return "Seu histórico mostra evolucão positiva e consistente."

    if trend == "CRITICA":
        return "Foi detectada deterioração acentuada " "que exige intervenção imediata."

    if pattern == "consistent_decline":
        return "Foi detectada deterioração recente " "no seu comportamento financeiro."

    if pattern == "high_oscillation":
        return (
            "Foram detectadas oscilacões relevantes "
            "que indicam comportamento inconsistente."
        )

    if trend == "ESTAVEL" and volatility == "low":
        return (
            "Seu padrão indica estabilidade moderada " "ao longo das últimas análises."
        )

    return "Seu histórico apresenta sinais mistos " "e precisa de mais análises."
