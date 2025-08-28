from __future__ import annotations

from pydantic import BaseModel


class SurfacedJobIn(BaseModel):
    """Payload for logging a surfaced job."""

    job_id: str
    agent_id: str
    user_id: str
