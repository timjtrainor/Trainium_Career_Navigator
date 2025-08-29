from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..services.evaluation import (
    JobNotFoundError,
    QueueError,
    queue_job_evaluation,
)

router = APIRouter()


@router.post("/api/evaluate/job/{job_id}", status_code=202)
def evaluate(job_id: str) -> dict[str, str]:
    """Trigger non-blocking evaluation of a job."""
    try:
        queue_job_evaluation(job_id)
    except JobNotFoundError:
        raise HTTPException(status_code=404, detail="job not found")
    except QueueError:
        raise HTTPException(status_code=500, detail="queue failure")
    return {"status": "queued", "job_id": job_id}
