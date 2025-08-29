from __future__ import annotations

from pydantic import BaseModel


class Recommendation(BaseModel):
    """Job recommendation derived from final decisions."""

    job_id: str
    title: str | None
    company: str | None
    url: str | None
    rationale: str | None
    confidence: float
