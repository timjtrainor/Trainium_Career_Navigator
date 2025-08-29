from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Query
from datetime import datetime

from ..models.feedback import Feedback, FeedbackIn
from ..services.feedback import list_feedback, save_feedback

router = APIRouter()


@router.post("/api/feedback", response_model=Feedback)
def submit_feedback(feedback: FeedbackIn) -> Feedback:
    """Store user feedback."""
    return save_feedback(feedback)


@router.get("/api/feedback", response_model=List[Feedback])
def get_feedback(
    job_id: Optional[str] = Query(None),
    agent_id: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
    start_ts: Optional[datetime] = Query(None),
    end_ts: Optional[datetime] = Query(None),
) -> List[Feedback]:
    """Return feedback entries filtered by job, agent, user, and time."""
    return list_feedback(job_id, agent_id, user_id, start_ts, end_ts)
