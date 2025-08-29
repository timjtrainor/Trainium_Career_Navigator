from __future__ import annotations

from math import ceil
from typing import List

from fastapi import APIRouter, HTTPException, Query

from ..models.job import (
    JobDetail,
    JobListResponse,
    JobOut,
    JobCreate,
    JobCreateResponse,
)
from ..services.jobs import create_job, get_job_detail, list_unique_jobs

router = APIRouter()


@router.get("/api/jobs/unique", response_model=JobListResponse)
def unique_jobs(
    query: str | None = None,
    company: str | None = None,
    source: List[str] | None = Query(default=None),
    since: str | None = Query(default=None, description="Relative window"),
    hide: List[str] | None = Query(default=None),
    page: int = 1,
) -> JobListResponse:
    """List jobs with optional filtering."""

    jobs, total = list_unique_jobs(
        query=query,
        company=company,
        sources=source,
        since=since,
        hide=hide,
        page=page,
        page_size=50,
    )
    page_count = ceil(total / 50) if total else 0
    data = [
        JobOut(
            id=j.job_id,
            title=j.title,
            company=j.company,
            url=j.url,
            source=j.source,
            updated_at=j.updated_at,
            decision=j.decision,
        )
        for j in jobs
    ]
    return JobListResponse(
        data=data,
        meta={"page": page, "page_count": page_count, "total": total},
    )


@router.get("/api/jobs/{job_id}", response_model=JobDetail)
def job_detail(job_id: str) -> JobDetail:
    """Fetch a job record with evaluation summary."""

    job = get_job_detail(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="job not found")
    return job


@router.post("/api/jobs", response_model=JobCreateResponse, status_code=201)
def log_job(payload: JobCreate) -> JobCreateResponse:
    """Log a job discovered externally."""

    try:
        return create_job(payload)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
