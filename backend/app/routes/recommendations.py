from __future__ import annotations

from typing import List

from fastapi import APIRouter

from ..models.recommendation import Recommendation
from ..services.recommendations import list_recommendations

router = APIRouter()


@router.get("/api/recommendations", response_model=List[Recommendation])
def recommendations() -> List[Recommendation]:
    """List jobs with a positive final decision."""
    return list_recommendations()
