from pathlib import Path
import sys

from fastapi import FastAPI
from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[2]))

from backend.app.routes.metrics import router


def test_metrics_endpoints(monkeypatch) -> None:
    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)

    monkeypatch.setattr("backend.app.routes.metrics.get_error_rate", lambda: 1.0)
    monkeypatch.setattr(
        "backend.app.routes.metrics.get_average_latency", lambda: 50.0
    )
    monkeypatch.setattr(
        "backend.app.routes.metrics.get_fit_accuracy", lambda: 0.8
    )
    monkeypatch.setattr(
        "backend.app.routes.metrics.count_false_positives", lambda: 2
    )
    monkeypatch.setattr(
        "backend.app.routes.metrics.get_missed_opportunities", lambda: 3
    )
    monkeypatch.setattr(
        "backend.app.routes.metrics.get_application_conversion",
        lambda: (0.25, 10),
    )

    resp = client.get("/api/metrics/operational")
    assert resp.status_code == 200
    assert resp.json()["avg_latency_ms"] == 50.0

    resp2 = client.get("/api/metrics/user")
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert data2["false_positives"] == 2
    assert data2["missed_opportunities"] == 3

    resp3 = client.get("/api/metrics/business")
    assert resp3.status_code == 200
    data3 = resp3.json()
    assert data3["application_volume"] == 10
