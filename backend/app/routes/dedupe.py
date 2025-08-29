from __future__ import annotations

from typing import List

from fastapi import APIRouter

from ..models.dedupe_review import DedupeReview
from ..services.dedupe import list_pending, record_decision

router = APIRouter()


@router.get("/api/dedupe/review", response_model=List[DedupeReview])
def list_reviews() -> List[DedupeReview]:
    """Return dedupe pairs awaiting review."""
    return list_pending()


@router.post("/api/dedupe/review/{review_id}/approve")
def approve_review(review_id: int) -> dict[str, str]:
    """Approve a dedupe pair."""
    record_decision(review_id, "approved")
    return {"status": "ok"}


@router.post("/api/dedupe/review/{review_id}/reject")
def reject_review(review_id: int) -> dict[str, str]:
    """Reject a dedupe pair."""
    record_decision(review_id, "rejected")
    return {"status": "ok"}

