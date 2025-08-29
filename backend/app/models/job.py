from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field
from typing import List


class Job(BaseModel):
    """Simplified job record."""

    job_id: str
    title: str | None = None
    company: str | None = None
    url: str | None = None
    source: str | None = None
    updated_at: datetime | None = None
    decision: str | None = None


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


class JobCreate(BaseModel):
    """Input model for logging an external job."""

    title: str
    company: str
    url: str
    location: str | None = None
    description: str | None = None


class JobCreateResponse(BaseModel):
    """Response model for a logged job."""

    id: str = Field(alias="job_id")
    status: str
    created_at: datetime


class PageMeta(BaseModel):
    """Metadata for paginated responses."""

    page: int
    page_count: int
    total: int


class JobOut(BaseModel):
    """Output model with user-facing field names."""

    id: str
    title: str | None = None
    company: str | None = None
    url: str | None = None
    source: str | None = None
    updated_at: datetime | None = None
    decision: str | None = None


class JobListResponse(BaseModel):
    """Paginated list of jobs."""

    data: List[JobOut]
    meta: PageMeta
