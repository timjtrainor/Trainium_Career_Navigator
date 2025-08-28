"""JobSpy FastAPI application."""

from __future__ import annotations

import logging
import os
import time
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

try:  # pragma: no cover - optional dependency
    import jobspy as jobspy_lib
except ImportError:  # pragma: no cover
    jobspy_lib = None


app = FastAPI(title="JobSpy API", version="0.1.0")

logger = logging.getLogger(__name__)


def scrape_jobs(source: str, *, search_term: str | None = None) -> dict[str, Any]:
    """Invoke the JobSpy scraping library for the given source."""

    if jobspy_lib is None:  # pragma: no cover - library not installed
        return {"jobs": [], "source": source}
    return jobspy_lib.scrape_jobs(source, search_term=search_term)  # type: ignore[attr-defined]


@app.get("/jobs/search", response_class=JSONResponse)
def search_jobs(
    source: str,
    search_term: str | None = None,
    google_search_term: str | None = None,
) -> dict[str, Any]:
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
    return scrape_jobs(source_l, search_term=term)

