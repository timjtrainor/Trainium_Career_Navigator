from __future__ import annotations

from pydantic import BaseModel


class ApplicationIn(BaseModel):
    """Payload for logging a job application."""

    job_id: str
    agent_id: str
    user_id: str
