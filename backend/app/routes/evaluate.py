from __future__ import annotations

from typing import List

from fastapi import APIRouter

from ..models.evaluation import PersonaEvaluation
from ..services.evaluation import evaluate_job

router = APIRouter()


@router.post("/api/evaluate/job/{job_id}", response_model=List[PersonaEvaluation])
def evaluate(job_id: str) -> List[PersonaEvaluation]:
    """Trigger motivational personas to evaluate a job."""
    return evaluate_job(job_id)
