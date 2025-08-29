from pathlib import Path
import sys

from fastapi import FastAPI
from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[2]))

from backend.app.routes.evaluate import router
from backend.app.services.evaluation import JobNotFoundError


def test_enqueue_evaluation(monkeypatch) -> None:
    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)

    called: list[str] = []

    def fake_queue(job_id: str) -> None:
        called.append(job_id)

    monkeypatch.setattr(
        "backend.app.routes.evaluate.queue_job_evaluation", fake_queue
    )

    resp = client.post("/api/evaluate/job/job1")
    assert resp.status_code == 202
    data = resp.json()
    assert data["status"] == "queued"
    assert called == ["job1"]


def test_enqueue_evaluation_not_found(monkeypatch) -> None:
    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)

    def fake_queue(job_id: str) -> None:
        raise JobNotFoundError

    monkeypatch.setattr(
        "backend.app.routes.evaluate.queue_job_evaluation", fake_queue
    )
    resp = client.post("/api/evaluate/job/job2")
    assert resp.status_code == 404
