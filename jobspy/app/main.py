"""JobSpy FastAPI application."""

from __future__ import annotations

import os
import time
from typing import Any, Sequence

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse


app = FastAPI(title="JobSpy API", version="0.1.0")


# Sources the API is allowed to query. Update this list when enabling new
# providers.
PERMITTED_SOURCES: Sequence[str] = ("indeed", "linkedin")


def scrape_jobs(source: str) -> dict[str, Any]:
    """Placeholder for the underlying job scraping implementation."""

    return {"jobs": [], "source": source}


@app.get("/jobs/search", response_class=JSONResponse)
def search_jobs(source: str, allowlist: str | None = None) -> dict[str, Any]:
    """Return mock job search results."""

    if source not in PERMITTED_SOURCES:
        raise HTTPException(status_code=400, detail="source not permitted")

    allowed = {s.strip().lower() for s in allowlist.split(",")} if allowlist else set()
    if allowed and source.lower() not in allowed:
        raise HTTPException(status_code=400, detail="source not allowlisted")

    delay = float(os.getenv("JOBSPY_DELAY_SECONDS", "1"))
    time.sleep(delay)
    return scrape_jobs(source)

