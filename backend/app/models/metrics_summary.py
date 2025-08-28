from __future__ import annotations

from pydantic import BaseModel


class OperationalMetrics(BaseModel):
    """Operational health metrics."""

    error_rate: float
    avg_latency_ms: float


class UserMetrics(BaseModel):
    """User experience metrics."""

    fit_accuracy: float
    false_positives: int
    missed_opportunities: int


class BusinessMetrics(BaseModel):
    """Business performance metrics."""

    application_rate: float
    application_volume: int
    conversion_ratio: float
