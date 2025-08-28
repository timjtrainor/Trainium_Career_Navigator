from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Query

from ..models.feedback import Feedback, FeedbackIn
from ..services.feedback import list_feedback, save_feedback

router = APIRouter()


@router.post("/api/feedback", response_model=Feedback)
def submit_feedback(feedback: FeedbackIn) -> Feedback:
    """Store user feedback."""
    return save_feedback(feedback)


@router.get("/api/feedback", response_model=List[Feedback])
def get_feedback(job_id: Optional[str] = Query(None)) -> List[Feedback]:
    """Return feedback entries, optionally filtered by job."""
    return list_feedback(job_id)
