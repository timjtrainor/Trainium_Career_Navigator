from datetime import datetime
from pathlib import Path
import sys

from fastapi import FastAPI
from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[2]))

from backend.app.models.feedback import Feedback
from backend.app.routes.feedback import router


def test_feedback_endpoints(monkeypatch) -> None:
    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)

    now = datetime.utcnow()
    sample = Feedback(
        job_id="job1",
        agent_id="agentA",
        user_id="userX",
        vote="up",
        comment="nice",
        timestamp=now,
    )

    def fake_save(feedback):
        assert feedback.job_id == "job1"
        return sample

    def fake_list(job_id=None):
        assert job_id == "job1"
        return [sample]

    monkeypatch.setattr("backend.app.routes.feedback.save_feedback", fake_save)
    monkeypatch.setattr("backend.app.routes.feedback.list_feedback", fake_list)

    resp = client.post(
        "/api/feedback",
        json={
            "job_id": "job1",
            "agent_id": "agentA",
            "user_id": "userX",
            "vote": "up",
            "comment": "nice",
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["job_id"] == "job1"

    resp2 = client.get("/api/feedback", params={"job_id": "job1"})
    assert resp2.status_code == 200
    items = resp2.json()
    assert len(items) == 1
    assert items[0]["vote"] == "up"
