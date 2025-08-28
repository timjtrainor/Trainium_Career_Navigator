"""JobSpy FastAPI application."""

from __future__ import annotations

import logging
import os
import time
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

try:  # pragma: no cover - optional dependency
    import jobspy as jobspy_lib
except ImportError:  # pragma: no cover
    jobspy_lib = None


class Job(BaseModel):
    """Normalized representation of a job posting."""

    title: str
    company: str | None = None
    description: str | None = None
    location: str | None = None
    url: str | None = None
    remote_status: str | None = None


class JobSearchResponse(BaseModel):
    """Response schema for `/jobs/search`."""

    source: str
    jobs: list[Job]


app = FastAPI(title="JobSpy API", version="0.1.0")

logger = logging.getLogger(__name__)


def scrape_jobs(source: str, *, search_term: str | None = None) -> dict[str, Any]:
    """Invoke the JobSpy scraping library for the given source."""

    if jobspy_lib is None:  # pragma: no cover - library not installed
        return {"jobs": [], "source": source}
    return jobspy_lib.scrape_jobs(source, search_term=search_term)  # type: ignore[attr-defined]


def normalize_job(raw: dict[str, Any]) -> Job:
    """Map provider-specific fields onto the normalized :class:`Job` schema."""

    remote = (
        raw.get("remote_status") or raw.get("is_remote") or raw.get("remote")
    )
    if isinstance(remote, bool):
        remote_status = "remote" if remote else "onsite"
    else:
        remote_status = remote

    return Job(
        title=raw.get("title") or raw.get("job_title") or "",
        company=raw.get("company") or raw.get("company_name"),
        description=raw.get("description") or raw.get("job_description"),
        location=raw.get("location") or raw.get("city") or raw.get("location_name"),
        url=raw.get("url") or raw.get("job_url") or raw.get("link"),
        remote_status=remote_status,
    )


@app.get("/jobs/search", response_class=JSONResponse, response_model=JobSearchResponse)
def search_jobs(
    source: str,
    search_term: str | None = None,
    google_search_term: str | None = None,
) -> JobSearchResponse:
    """Scrape jobs from the requested source."""

    if os.getenv("JOBSPY_ENABLED", "true").lower() != "true":
        raise HTTPException(status_code=501, detail="scraping disabled")

    allowed = {
        s.strip().lower()
        for s in os.getenv("JOBSPY_SOURCES", "indeed,linkedin,google").split(",")
        if s.strip()
    }

    if not allowed:
        raise HTTPException(status_code=501, detail="scraping disabled")

    source_l = source.lower()
    if source_l not in allowed:
        if source_l == "google":
            raise HTTPException(status_code=403, detail="Google not allowlisted")
        raise HTTPException(status_code=400, detail="source not allowlisted")

    delay = int(os.getenv("JOBSPY_DELAY_SECONDS", "2"))

    if source_l == "google":
        if not google_search_term:
            raise HTTPException(
                status_code=400,
                detail="google_search_term required for Google Jobs",
            )
        logger.info("Scraping Google Jobs with delay=%ss", delay)
        term = google_search_term
    else:
        term = search_term

    logger.info("Applied delay of %ss before scrape", delay)
    time.sleep(delay)
    raw = scrape_jobs(source_l, search_term=term)
    jobs = [normalize_job(j) for j in raw.get("jobs", [])]
    return JobSearchResponse(source=source_l, jobs=jobs)

