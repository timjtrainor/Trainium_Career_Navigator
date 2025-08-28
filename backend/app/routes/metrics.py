from __future__ import annotations

from typing import List

from fastapi import APIRouter

from ..models.application import ApplicationIn
from ..models.metric import Metric
from ..models.metrics_summary import (
    BusinessMetrics,
    OperationalMetrics,
    UserMetrics,
)
from ..models.surfaced_job import SurfacedJobIn
from ..services.metrics import (
    count_false_positives,
    get_application_conversion,
    get_average_latency,
    get_error_rate,
    get_fit_accuracy,
    get_metrics,
    get_missed_opportunities,
    log_application,
    log_surfaced_job,
)

router = APIRouter()


@router.get("/api/metrics/operational", response_model=OperationalMetrics)
def operational_metrics() -> OperationalMetrics:
    """Return operational metrics."""
    rate = get_error_rate()
    latency = get_average_latency()
    return OperationalMetrics(error_rate=rate, avg_latency_ms=latency)


@router.get("/api/metrics/user", response_model=UserMetrics)
def user_metrics() -> UserMetrics:
    """Return user experience metrics."""
    acc = get_fit_accuracy()
    false = count_false_positives()
    missed = get_missed_opportunities()
    return UserMetrics(
        fit_accuracy=acc,
        false_positives=false,
        missed_opportunities=missed,
    )


@router.get("/api/metrics/business", response_model=BusinessMetrics)
def business_metrics() -> BusinessMetrics:
    """Return business performance metrics."""
    rate, volume = get_application_conversion()
    return BusinessMetrics(
        application_rate=rate,
        application_volume=volume,
        conversion_ratio=rate,
    )


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


@router.post("/api/metrics/application")
def application(payload: ApplicationIn) -> dict[str, str]:
    """Log when a user applies to a surfaced job."""
    log_application(payload.job_id, payload.user_id, payload.agent_id)
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


@router.get("/api/metrics/application_conversion")
def application_conversion() -> dict[str, float | int]:
    """Return recent application conversion metrics."""
    rate, volume = get_application_conversion()
    return {"application_rate": rate, "application_volume": volume}
