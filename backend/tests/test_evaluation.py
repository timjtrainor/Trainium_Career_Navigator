from pathlib import Path
import sys

from fastapi import FastAPI
from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[2]))

from backend.app.models.evaluation import PersonaEvaluation
from backend.app.routes.evaluate import router


def test_evaluate_job(monkeypatch) -> None:
    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)

    sample = [
        PersonaEvaluation(persona="builder", vote_bool=True, rationale_text="grow"),
        PersonaEvaluation(persona="maximizer", vote_bool=False, rationale_text="low"),
        PersonaEvaluation(persona="harmonizer", vote_bool=True, rationale_text="fit"),
        PersonaEvaluation(persona="pathfinder", vote_bool=True, rationale_text="align"),
        PersonaEvaluation(persona="adventurer", vote_bool=False, rationale_text="boring"),
    ]

    def fake_eval(job_id: str):
        assert job_id == "job1"
        return sample

    monkeypatch.setattr("backend.app.routes.evaluate.evaluate_job", fake_eval)

    resp = client.post("/api/evaluate/job/job1")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 5
    assert data[0]["persona"] == "builder"
    assert "vote_bool" in data[0]
