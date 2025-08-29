from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel


class Job(BaseModel):
    """Simplified job record."""

    job_id: str
    title: str | None = None
    company: str | None = None
    url: str | None = None
    source: str | None = None
    updated_at: datetime | None = None


class EvaluationSummary(BaseModel):
    """Aggregated evaluation results for a job."""

    yes: int
    no: int
    final_decision_bool: bool | None = None
    confidence: float | None = None


class JobDetail(Job):
    """Job record with evaluation summary."""

    description: str | None = None
    location: str | None = None
    evaluation: EvaluationSummary
