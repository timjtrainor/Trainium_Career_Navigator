from __future__ import annotations

from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException, Query

from ..models.job import Job, JobDetail
from ..services.jobs import get_job_detail, list_unique_jobs

router = APIRouter()


@router.get("/api/jobs/unique", response_model=List[Job])
def unique_jobs(
    query: str | None = None,
    company: str | None = None,
    source: str | None = None,
    since: datetime | None = Query(default=None, description="ISO timestamp"),
    limit: int = 50,
    offset: int = 0,
) -> List[Job]:
    """List jobs with optional filtering."""

    return list_unique_jobs(
        query=query,
        company=company,
        source=source,
        since=since,
        limit=limit,
        offset=offset,
    )


@router.get("/api/jobs/{job_id}", response_model=JobDetail)
def job_detail(job_id: str) -> JobDetail:
    """Fetch a job record with evaluation summary."""

    job = get_job_detail(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="job not found")
    return job
