"""JobSpy FastAPI application."""

from __future__ import annotations

import asyncio
import logging
import os
import time
import uuid
from contextlib import contextmanager
from time import perf_counter
from typing import Any

import psycopg2
from psycopg2.extensions import cursor as PGCursor
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

VALID_SOURCES = {"indeed", "linkedin", "google"}


class IngestionRun(BaseModel):
    """Record of a single ingestion run."""

    run_id: str
    board: str
    fetched: int
    normalized: int
    unique_new: int
    errors: int
    timestamp: float


# Structured logging helper
@contextmanager
def _log_stage(run_id: str, board: str, stage: str) -> Any:
    start = perf_counter()
    try:
        yield
    except Exception as exc:
        duration = perf_counter() - start
        logger.error(
            "stage failed",
            extra={
                "run_id": run_id,
                "board": board,
                "stage": stage,
                "duration": duration,
                "status": "error",
            },
        )
        raise
    else:
        duration = perf_counter() - start
        logger.info(
            "stage complete",
            extra={
                "run_id": run_id,
                "board": board,
                "stage": stage,
                "duration": duration,
                "status": "ok",
            },
        )


# Board-specific scheduling configuration
BOARD_CONFIG: dict[str, dict[str, Any]] = {
    "indeed": {
        "enabled": True,
        "cadence": "4h",
        "results_wanted_max": 50,
        "hours_old": 24,
        "country": "us",
        "delay": 0,
    },
    "linkedin": {
        "enabled": True,
        "cadence": "daily",
        "results_wanted_max": 50,
        "hours_old": 24,
        "country": "us",
        "delay": 0,
    },
}

# Track last run time for each board and all run records
_LAST_RUN: dict[str, float | None] = {b: None for b in BOARD_CONFIG}
INGESTION_RUNS: list[IngestionRun] = []


def _pg_connect() -> psycopg2.extensions.connection:
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        dbname=os.getenv("POSTGRES_DB"),
    )


def _ensure_jobs_table(cur: PGCursor) -> None:
    cur.execute(
        "CREATE TABLE IF NOT EXISTS jobs_normalized ("
        "id SERIAL PRIMARY KEY, "
        "source TEXT NOT NULL, "
        "title TEXT NOT NULL, "
        "company TEXT, "
        "description TEXT, "
        "location TEXT, "
        "url TEXT, "
        "is_remote BOOLEAN, "
        "job_id_ext TEXT NOT NULL, "
        "updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), "
        "UNIQUE (source, job_id_ext))"
    )


def _ensure_ingestion_runs_table(cur: PGCursor) -> None:
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS ingestion_runs (
            run_id UUID PRIMARY KEY,
            board TEXT NOT NULL,
            fetched INTEGER NOT NULL,
            normalized INTEGER NOT NULL,
            unique_new INTEGER NOT NULL,
            errors INTEGER NOT NULL,
            timestamp TIMESTAMPTZ NOT NULL
        )
        """
    )


def scrape_jobs(
    source: str,
    *,
    search_term: str | None = None,
    hours_old: int | None = None,
    results_wanted_max: int | None = None,
    country: str | None = None,
    delay: int | None = None,
) -> dict[str, Any]:
    """Invoke the JobSpy scraping library for the given source."""

    if jobspy_lib is None:  # pragma: no cover - library not installed
        return {"jobs": [], "source": source}
    return jobspy_lib.scrape_jobs(
        source,
        search_term=search_term,
        hours_old=hours_old,
        results_wanted_max=results_wanted_max,
        country=country,
        delay=delay,
    )  # type: ignore[attr-defined]


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


def normalize_for_db(source: str, raw: dict[str, Any]) -> dict[str, Any]:
    """Normalize a raw job for database persistence."""

    job = normalize_job(raw)
    is_remote = job.remote_status == "remote"
    job_id_ext = (
        raw.get("job_id")
        or raw.get("id")
        or raw.get("jobkey")
        or raw.get("job_id_ext")
        or job.url
    )
    return {
        "source": source,
        "title": job.title,
        "company": job.company,
        "description": job.description,
        "location": job.location,
        "url": job.url,
        "is_remote": is_remote,
        "job_id_ext": job_id_ext,
    }


@app.get("/jobs/search", response_class=JSONResponse, response_model=JobSearchResponse)
def search_jobs(
    source: str,
    search_term: str | None = None,
    google_search_term: str | None = None,
) -> JobSearchResponse:
    """Scrape jobs from the requested source."""

    if os.getenv("JOBSPY_ENABLED", "false").lower() != "true":
        raise HTTPException(status_code=501, detail="scraping disabled")

    allowed_raw = [
        s.strip().lower()
        for s in os.getenv("JOBSPY_SOURCES", "").split(",")
        if s.strip()
    ]
    if any(s not in VALID_SOURCES for s in allowed_raw):
        raise HTTPException(status_code=500, detail="invalid JOBSPY_SOURCES")
    allowed = set(allowed_raw)

    if not allowed:
        raise HTTPException(status_code=501, detail="scraping disabled")

    source_l = source.lower()
    if source_l not in allowed:
        if source_l == "google":
            raise HTTPException(status_code=403, detail="Google not allowlisted")
        raise HTTPException(status_code=400, detail="source not allowlisted")

    delay_str = os.getenv("JOBSPY_DELAY_SECONDS", "2")
    try:
        delay = int(delay_str)
    except ValueError as exc:
        raise HTTPException(
            status_code=500, detail="invalid JOBSPY_DELAY_SECONDS"
        ) from exc
    if delay < 0:
        raise HTTPException(status_code=500, detail="invalid JOBSPY_DELAY_SECONDS")

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
    limit = BOARD_CONFIG.get(source_l, {}).get("results_wanted_max")
    raw = scrape_jobs(source_l, search_term=term, results_wanted_max=limit)
    raw_jobs = raw.get("jobs", [])
    if limit is not None:
        raw_jobs = raw_jobs[:limit]
    jobs = [normalize_job(j) for j in raw_jobs]
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
    run_id = str(uuid.uuid4())
    start_all = perf_counter()
    cfg = BOARD_CONFIG[board]
    limit = cfg.get("results_wanted_max")
    with _log_stage(run_id, board, "scrape"):
        raw = scrape_jobs(
            board,
            hours_old=cfg.get("hours_old"),
            results_wanted_max=limit,
            country=cfg.get("country"),
            delay=cfg.get("delay"),
        )
        jobs = raw.get("jobs", [])
        if limit is not None:
            jobs = jobs[:limit]
    with _log_stage(run_id, board, "normalize"):
        normalized_jobs = [normalize_for_db(board, j) for j in jobs]
    unique_new = 0
    errors = 0
    ts = now or time.time()
    conn: psycopg2.extensions.connection | None = None
    with _log_stage(run_id, board, "persist"):
        try:
            conn = _pg_connect()
            with conn:
                with conn.cursor() as cur:
                    _ensure_jobs_table(cur)
                    _ensure_ingestion_runs_table(cur)
                    for job in normalized_jobs:
                        cur.execute(
                            """
                            INSERT INTO jobs_normalized
                                (source, title, company, description, location, url,
                                 is_remote, job_id_ext)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (source, job_id_ext) DO UPDATE SET
                                title = EXCLUDED.title,
                                company = EXCLUDED.company,
                                description = EXCLUDED.description,
                                location = EXCLUDED.location,
                                url = EXCLUDED.url,
                                is_remote = EXCLUDED.is_remote,
                                updated_at = NOW()
                            RETURNING xmax = 0
                            """,
                            (
                                job["source"],
                                job["title"],
                                job["company"],
                                job["description"],
                                job["location"],
                                job["url"],
                                job["is_remote"],
                                job["job_id_ext"],
                            ),
                        )
                        if cur.fetchone()[0]:
                            unique_new += 1
                    cur.execute(
                        """
                        INSERT INTO ingestion_runs
                            (run_id, board, fetched, normalized, unique_new, errors,
                             timestamp)
                        VALUES (%s, %s, %s, %s, %s, %s, TO_TIMESTAMP(%s))
                        """,
                        (
                            run_id,
                            board,
                            len(jobs),
                            len(normalized_jobs),
                            unique_new,
                            errors,
                            ts,
                        ),
                    )
        except Exception as exc:  # pragma: no cover - best effort
            errors += 1
            logger.warning("database unavailable, skipping persistence: %s", exc)
        finally:
            if conn is not None:
                conn.close()
    run = IngestionRun(
        run_id=run_id,
        board=board,
        fetched=len(jobs),
        normalized=len(normalized_jobs),
        unique_new=unique_new,
        errors=errors,
        timestamp=ts,
    )
    INGESTION_RUNS.append(run)
    _LAST_RUN[board] = run.timestamp
    logger.info(
        "ingest complete",
        extra={
            "run_id": run_id,
            "board": board,
            "stage": "complete",
            "duration": perf_counter() - start_all,
            "status": "ok",
        },
    )
    return run


def run_all_due(*, now: float | None = None) -> list[IngestionRun]:
    runs: list[IngestionRun] = []
    now = now or time.time()
    for board, cfg in BOARD_CONFIG.items():
        if cfg.get("enabled") and _due(board, now=now):
            runs.append(ingest_board(board, now=now))
    return runs


@app.post("/ingest/run", response_model=IngestionRun)
async def run_single(board: str) -> IngestionRun:
    if board not in BOARD_CONFIG:
        raise HTTPException(status_code=404, detail="unknown board")
    if not BOARD_CONFIG[board].get("enabled", True):
        raise HTTPException(status_code=400, detail="board disabled")
    return await asyncio.to_thread(ingest_board, board)


@app.get("/ingest/runs", response_model=list[IngestionRun])
def list_runs(limit: int = 100) -> list[IngestionRun]:
    try:
        conn = _pg_connect()
        with conn, conn.cursor() as cur:
            cur.execute(
                """
                SELECT run_id, board, fetched, normalized, unique_new, errors,
                       EXTRACT(EPOCH FROM timestamp)
                FROM ingestion_runs
                ORDER BY timestamp DESC
                LIMIT %s
                """,
                (limit,),
            )
            rows = cur.fetchall()
        return [
            IngestionRun(
                run_id=r[0],
                board=r[1],
                fetched=r[2],
                normalized=r[3],
                unique_new=r[4],
                errors=r[5],
                timestamp=r[6],
            )
            for r in rows
        ]
    except Exception:  # pragma: no cover - fallback to memory
        return INGESTION_RUNS[-limit:]


@app.post("/ingest/run-all", response_model=list[IngestionRun])
async def run_all_endpoint() -> list[IngestionRun]:
    return await asyncio.to_thread(run_all_due)


async def _scheduler_loop() -> None:
    interval = int(os.getenv("INGEST_SCHEDULER_INTERVAL_SECONDS", "3600"))
    while True:
        await asyncio.to_thread(run_all_due)
        await asyncio.sleep(interval)


@app.on_event("startup")
async def _startup() -> None:  # pragma: no cover - background task
    asyncio.create_task(_scheduler_loop())

