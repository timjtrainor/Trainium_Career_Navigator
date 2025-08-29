from datetime import datetime
from pathlib import Path
import sys

from fastapi import FastAPI
from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[2]))

from backend.app.models.dedupe_review import DedupeReview
from backend.app.routes.dedupe import router


def test_dedupe_review_endpoints(monkeypatch) -> None:
    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)

    sample = DedupeReview(
        id=1,
        job_id_1=1,
        job_id_2=2,
        similarity=0.83,
        status="pending",
        created_at=datetime.utcnow(),
        reviewed_at=None,
    )

    def fake_list() -> list[DedupeReview]:
        return [sample]

    def fake_record(review_id: int, decision: str) -> None:
        assert review_id == 1
        assert decision in {"approved", "rejected"}

    monkeypatch.setattr("backend.app.routes.dedupe.list_pending", fake_list)
    monkeypatch.setattr("backend.app.routes.dedupe.record_decision", fake_record)

    resp = client.get("/api/dedupe/review")
    assert resp.status_code == 200
    items = resp.json()
    assert items[0]["id"] == 1

    resp2 = client.post("/api/dedupe/review/1/approve")
    assert resp2.status_code == 200

    resp3 = client.post("/api/dedupe/review/1/reject")
    assert resp3.status_code == 200
