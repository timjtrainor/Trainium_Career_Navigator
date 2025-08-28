from __future__ import annotations

from typing import List

from fastapi import APIRouter

from ..models.metric import Metric
from ..models.surfaced_job import SurfacedJobIn
from ..services.metrics import (
    count_false_positives,
    get_error_rate,
    get_fit_accuracy,
    get_metrics,
    log_surfaced_job,
)

router = APIRouter()


@router.get("/api/metrics/error_rate")
def error_rate() -> dict[str, float]:
    """Return the rolling 7-day error rate."""
    rate = get_error_rate()
    return {"error_rate": rate}


@router.get("/api/metrics", response_model=List[Metric])
def list_metrics() -> List[Metric]:
    """Return recent request metrics."""
    return get_metrics()


@router.post("/api/metrics/surfaced_job")
def surfaced_job(payload: SurfacedJobIn) -> dict[str, str]:
    """Log when a job is surfaced to a user."""
    log_surfaced_job(payload.job_id, payload.user_id, payload.agent_id)
    return {"status": "ok"}


@router.get("/api/metrics/fit_accuracy")
def fit_accuracy() -> dict[str, float]:
    """Return the rolling 7-day fit accuracy."""
    acc = get_fit_accuracy()
    return {"fit_accuracy": acc}


@router.get("/api/metrics/false_positives")
def false_positives() -> dict[str, int]:
    """Return the count of recent false positives."""
    count = count_false_positives()
    return {"false_positives": count}
