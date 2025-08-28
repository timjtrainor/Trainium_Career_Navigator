from __future__ import annotations

from typing import Any, List

from fastapi import APIRouter

from ..services.personas_loader import load_personas

router = APIRouter()


@router.get("/api/personas")
def list_personas() -> List[dict[str, Any]]:
    """Return the catalog of personas for the frontend."""
    personas = load_personas()
    return [p.model_dump() for p in personas]
