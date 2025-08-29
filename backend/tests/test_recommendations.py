from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))

from backend.app.services import recommendations as rec_service
from backend.app.models.recommendation import Recommendation
from fastapi import FastAPI
from fastapi.testclient import TestClient


class FakeCursor:
    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple | None]] = []
        self.last_query = ""

    def execute(self, query: str, params: tuple | None = None) -> None:
        self.calls.append((query, params))
        self.last_query = query

    def fetchall(self):
        if "FROM decisions" in self.last_query:
            return [("job1", 0.75)]
        return []

    def fetchone(self):
        if "FROM jobs_normalized" in self.last_query:
            return ("Engineer", "Acme", "http://a")
        if "FROM evaluations" in self.last_query:
            return ("Great role",)
        return None

    def close(self) -> None:  # pragma: no cover - no action
        pass


class FakeConn:
    def __init__(self) -> None:
        self.cursor_obj = FakeCursor()

    def cursor(self):
        return self.cursor_obj

    def commit(self) -> None:  # pragma: no cover - no action
        pass

    def close(self) -> None:  # pragma: no cover - no action
        pass


def test_list_recommendations(monkeypatch) -> None:
    fake = FakeConn()
    monkeypatch.setattr(rec_service, "_get_conn", lambda: fake)
    recs = rec_service.list_recommendations()
    assert len(recs) == 1
    rec = recs[0]
    assert isinstance(rec, Recommendation)
    assert rec.job_id == "job1"
    assert rec.title == "Engineer"
    assert rec.company == "Acme"
    assert rec.url == "http://a"
    assert rec.rationale == "Great role"
    assert rec.confidence == 0.75
    eval_calls = [
        c for c in fake.cursor_obj.calls if "FROM evaluations" in c[0]
    ]
    assert eval_calls and "persona = %s" in eval_calls[0][0]


def test_api_recommendations(monkeypatch) -> None:
    app = FastAPI()
    from backend.app.routes import recommendations as route_module

    monkeypatch.setattr(
        route_module,
        "list_recommendations",
        lambda: [
            Recommendation(
                job_id="job1",
                title="Engineer",
                company="Acme",
                url="http://a",
                rationale="Great role",
                confidence=0.75,
            )
        ],
    )
    app.include_router(route_module.router)
    client = TestClient(app)
    resp = client.get("/api/recommendations")
    assert resp.status_code == 200
    data = resp.json()
    assert data[0]["job_id"] == "job1"
