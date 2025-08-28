from __future__ import annotations

from typing import List

from fastapi import APIRouter

from ..models.metric import Metric
from ..services.metrics import get_error_rate, get_metrics

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
