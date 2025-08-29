from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel


class DedupeReview(BaseModel):
    """Record of a dedupe candidate pair."""

    id: int
    job_id_1: int
    job_id_2: int
    similarity: float
    status: str
    created_at: datetime
    reviewed_at: datetime | None = None
