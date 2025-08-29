from datetime import datetime
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))

from backend.app.services import jobs as jobs_service
from backend.app.models.job import (
    EvaluationSummary,
    Job,
    JobCreateResponse,
    JobDetail,
)
from fastapi import FastAPI
from fastapi.testclient import TestClient


class FakeCursorList:
    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple | None]] = []

    def execute(self, query: str, params: tuple | None = None) -> None:
        self.calls.append((query, params))

    def fetchall(self):
        return [
            (
                "id1",
                "Engineer",
                "Acme",
                "http://a",
                "indeed",
                datetime(2024, 1, 1),
                "undecided",
            )
        ]

    def close(self) -> None:  # pragma: no cover - no action
        pass


class FakeConnList:
    def __init__(self) -> None:
        self.cursor_obj = FakeCursorList()

    def cursor(self):
        return self.cursor_obj

    def close(self) -> None:  # pragma: no cover - no action
        pass


class FakeCursorDetail:
    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple | None]] = []

    def execute(self, query: str, params: tuple | None = None) -> None:
        self.calls.append((query, params))

    def fetchone(self):
        last = self.calls[-1][0]
        if "FROM jobs_normalized" in last:
            return (
                "id1",
                "Engineer",
                "Acme",
                "Desc",
                "Remote",
                "http://a",
                "indeed",
                datetime(2024, 1, 1),
            )
        if "FROM decisions" in last:
            return (True, 0.9)
        return None

    def fetchall(self):
        last = self.calls[-1][0]
        if "FROM evaluations" in last:
            return [(True, 2), (False, 1)]
        return []

    def close(self) -> None:  # pragma: no cover - no action
        pass


class FakeConnDetail:
    def __init__(self) -> None:
        self.cursor_obj = FakeCursorDetail()

    def cursor(self):
        return self.cursor_obj

    def close(self) -> None:  # pragma: no cover - no action
        pass


def test_list_unique_jobs(monkeypatch) -> None:
    fake = FakeConnList()

    def fake_fetchone():
        return (1,)

    fake.cursor_obj.fetchone = fake_fetchone  # type: ignore[attr-defined]
    monkeypatch.setattr(jobs_service, "_get_conn", lambda: fake)
    jobs, total = jobs_service.list_unique_jobs()
    assert total == 1
    assert len(jobs) == 1
    job = jobs[0]
    assert isinstance(job, Job)
    assert job.job_id == "id1"
    assert job.decision == "undecided"


def test_get_job_detail(monkeypatch) -> None:
    fake = FakeConnDetail()
    monkeypatch.setattr(jobs_service, "_get_conn", lambda: fake)
    detail = jobs_service.get_job_detail("id1")
    assert isinstance(detail, JobDetail)
    assert detail.evaluation.yes == 2
    assert detail.evaluation.no == 1
    assert detail.evaluation.final_decision_bool is True
    assert abs(detail.evaluation.confidence - 0.9) < 1e-6


def test_jobs_api(monkeypatch) -> None:
    app = FastAPI()
    from backend.app.routes import jobs as jobs_route

    monkeypatch.setattr(
        jobs_route,
        "list_unique_jobs",
        lambda **_: (
            [
                Job(
                    job_id="id1",
                    title="Engineer",
                    company="Acme",
                    url="http://a",
                    source="indeed",
                    updated_at=datetime(2024, 1, 1),
                    decision="undecided",
                )
            ],
            1,
        ),
    )
    monkeypatch.setattr(
        jobs_route,
        "get_job_detail",
        lambda job_id: JobDetail(
            job_id=job_id,
            title="Engineer",
            company="Acme",
            url="http://a",
            source="indeed",
            updated_at=datetime(2024, 1, 1),
            description="Desc",
            location="Remote",
            evaluation=EvaluationSummary(yes=2, no=1, final_decision_bool=True, confidence=0.9),
        ),
    )
    monkeypatch.setattr(
        jobs_route,
        "create_job",
        lambda payload: JobCreateResponse(job_id="id2", status="logged", created_at=datetime(2024, 1, 1)),
    )
    app.include_router(jobs_route.router)
    client = TestClient(app)
    resp = client.get("/api/jobs/unique")
    assert resp.status_code == 200
    data = resp.json()
    assert data["data"][0]["id"] == "id1"
    assert data["meta"]["total"] == 1
    resp = client.get("/api/jobs/id1")
    assert resp.status_code == 200
    detail = resp.json()
    assert detail["evaluation"]["yes"] == 2
    resp = client.post(
        "/api/jobs",
        json={"title": "Eng", "company": "Acme", "url": "http://a"},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["status"] == "logged"


def test_log_job_duplicate(monkeypatch) -> None:
    app = FastAPI()
    from backend.app.routes import jobs as jobs_route

    def dup(_payload):
        raise ValueError("duplicate job")

    monkeypatch.setattr(jobs_route, "create_job", dup)
    app.include_router(jobs_route.router)
    client = TestClient(app)
    resp = client.post(
        "/api/jobs",
        json={"title": "Eng", "company": "Acme", "url": "http://a"},
    )
    assert resp.status_code == 409
