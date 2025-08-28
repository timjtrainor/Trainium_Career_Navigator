from typing import Any

from fastapi import FastAPI
from fastapi.responses import JSONResponse


app = FastAPI(title="JobSpy API", version="0.1.0")


@app.get("/jobs/search", response_class=JSONResponse)
def search_jobs() -> dict[str, Any]:
    """Return mock job search results."""
    return {"jobs": []}
