"""JobSpy FastAPI application."""

from __future__ import annotations

import asyncio
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

# Simple in-memory cache for search results
CACHE_TTL = int(os.getenv("JOBSPY_CACHE_TTL_SECONDS", "600"))
_CACHE: dict[tuple[str, str], tuple[float, JobSearchResponse]] = {}


class IngestionRun(BaseModel):
    """Record of a single ingestion run."""

    board: str
    fetched: int
    normalized: int
    unique_new: int
    errors: int
    timestamp: float


# Board-specific scheduling configuration
BOARD_CONFIG: dict[str, dict[str, Any]] = {
    "indeed": {
        "enabled": True,
        "cadence": "4h",
        "results_wanted_max": 50,
        "hours_old": 24,
        "delay_seconds": 0,
    },
    "linkedin": {
        "enabled": True,
        "cadence": "daily",
        "results_wanted_max": 50,
        "hours_old": 24,
        "delay_seconds": 0,
    },
}

# Track last run time for each board and all run records
_LAST_RUN: dict[str, float | None] = {b: None for b in BOARD_CONFIG}
INGESTION_RUNS: list[IngestionRun] = []


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

    cache_key = (source_l, term or "")
    now = time.time()
    cached = _CACHE.get(cache_key)
    if cached and now - cached[0] < CACHE_TTL:
        logger.info("Returning cached result for %s", cache_key)
        return cached[1]

    logger.info("Applied delay of %ss before scrape", delay)
    time.sleep(delay)
    raw = scrape_jobs(source_l, search_term=term)
    jobs = [normalize_job(j) for j in raw.get("jobs", [])]
    response = JobSearchResponse(source=source_l, jobs=jobs)
    _CACHE[cache_key] = (time.time(), response)
    return response


def _interval_for(board: str) -> float:
    cadence = BOARD_CONFIG[board]["cadence"].lower()
    return 4 * 3600 if cadence == "4h" else 24 * 3600


def _due(board: str, *, now: float | None = None) -> bool:
    now = now or time.time()
    last = _LAST_RUN.get(board)
    return last is None or now - last >= _interval_for(board)


def ingest_board(board: str, *, now: float | None = None) -> IngestionRun:
    cfg = BOARD_CONFIG[board]
    time.sleep(cfg.get("delay_seconds", 0))
    raw = scrape_jobs(board)
    jobs = raw.get("jobs", [])
    jobs = jobs[: cfg.get("results_wanted_max", len(jobs))]
    normalized_jobs = [normalize_job(j) for j in jobs]
    run = IngestionRun(
        board=board,
        fetched=len(jobs),
        normalized=len(normalized_jobs),
        unique_new=len(normalized_jobs),
        errors=0,
        timestamp=now or time.time(),
    )
    INGESTION_RUNS.append(run)
    _LAST_RUN[board] = run.timestamp
    return run


def run_all_due(*, now: float | None = None) -> list[IngestionRun]:
    runs: list[IngestionRun] = []
    now = now or time.time()
    for board, cfg in BOARD_CONFIG.items():
        if cfg.get("enabled") and _due(board, now=now):
            runs.append(ingest_board(board, now=now))
    return runs


@app.post("/ingest/run", response_model=IngestionRun)
def run_single(board: str) -> IngestionRun:
    if board not in BOARD_CONFIG:
        raise HTTPException(status_code=404, detail="unknown board")
    if not BOARD_CONFIG[board].get("enabled", True):
        raise HTTPException(status_code=400, detail="board disabled")
    return ingest_board(board)


@app.post("/ingest/run-all", response_model=list[IngestionRun])
def run_all_endpoint() -> list[IngestionRun]:
    return run_all_due()


async def _scheduler_loop() -> None:
    interval = int(os.getenv("INGEST_SCHEDULER_INTERVAL_SECONDS", "3600"))
    while True:
        run_all_due()
        await asyncio.sleep(interval)


@app.on_event("startup")
async def _startup() -> None:  # pragma: no cover - background task
    asyncio.create_task(_scheduler_loop())

