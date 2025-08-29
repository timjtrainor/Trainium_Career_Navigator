from __future__ import annotations

from pydantic import BaseModel


class PersonaEvaluation(BaseModel):
    """Result of evaluating a job from a persona's perspective."""

    persona: str
    vote_bool: bool | None
    rationale_text: str
