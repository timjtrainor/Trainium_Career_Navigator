from __future__ import annotations

from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel


class FeedbackIn(BaseModel):
    """Payload for submitting feedback."""

    job_id: str
    agent_id: str
    user_id: str
    vote: Literal["up", "down"]
    comment: Optional[str] = None


class Feedback(FeedbackIn):
    """Represents stored feedback."""

    timestamp: datetime
