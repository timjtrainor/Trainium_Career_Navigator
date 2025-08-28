from __future__ import annotations

from typing import Dict, List, Literal

from pydantic import BaseModel


class Persona(BaseModel):
    """Represents a Trainium persona definition."""

    id: str
    name: str
    category: Literal["advisory", "motivational", "decision"]
    summary: str
    decision_lens: str
    tone: str
    capabilities: List[str]
    crew_manifest_ref: str
    provider_map: Dict[str, str]
