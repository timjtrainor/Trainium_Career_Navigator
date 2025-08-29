from __future__ import annotations

from pydantic import BaseModel


class Decision(BaseModel):
    """Final decision for a job after aggregation."""

    job_id: str
    final_decision_bool: bool
    confidence: float
    method: str
