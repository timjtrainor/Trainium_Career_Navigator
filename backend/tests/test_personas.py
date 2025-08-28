from pathlib import Path
import sys

from fastapi import FastAPI
from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[2]))

from backend.app.routes.personas import router
from backend.app.services.personas_loader import load_personas


def test_load_personas() -> None:
    personas = load_personas()
    assert len(personas) == 23
    assert personas[0].id == "headhunter"
    categories = [p.category for p in personas]
    assert categories.count("advisory") == 14
    assert categories.count("motivational") == 5
    assert categories.count("decision") == 4


def test_api_personas() -> None:
    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)
    resp = client.get("/api/personas")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 23
    first = data[0]
    expected = {
        "id",
        "name",
        "category",
        "summary",
        "decision_lens",
        "tone",
        "capabilities",
        "crew_manifest_ref",
        "provider_map",
    }
    assert expected.issubset(first.keys())
