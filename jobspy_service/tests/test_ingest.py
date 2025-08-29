from pathlib import Path
import sys
from typing import Any
from unittest.mock import patch

import pytest

sys.path.append(str(Path(__file__).resolve().parents[2]))
import jobspy_service.app.main as main


@pytest.mark.anyio
async def test_run_records_ingestion(monkeypatch, client):
    main.INGESTION_RUNS.clear()
    main.BOARD_CONFIG["demo"] = {
        "enabled": True,
        "cadence": "4h",
        "results_wanted_max": 10,
        "hours_old": 24,
        "delay_seconds": 0,
    }
    main._LAST_RUN["demo"] = None

    sample = {"jobs": [{"title": "Dev"}]}

    with patch("jobspy_service.app.main.scrape_jobs", return_value=sample):
        response = await client.post("/ingest/run", params={"board": "demo"})

    assert response.status_code == 200
    body = response.json()
    assert body["board"] == "demo"
    assert body["fetched"] == 1
    assert "run_id" in body
    assert len(main.INGESTION_RUNS) == 1
    list_resp = await client.get("/ingest/runs")
    runs = list_resp.json()
    assert any(r["run_id"] == body["run_id"] for r in runs)


@pytest.mark.anyio
async def test_results_capped_per_board(monkeypatch):
    main.INGESTION_RUNS.clear()
    main.BOARD_CONFIG["demo"] = {
        "enabled": True,
        "cadence": "4h",
        "results_wanted_max": 3,
        "hours_old": 24,
        "delay": 0,
    }
    sample_job = {"title": "Dev"}
    sample = {"jobs": [sample_job for _ in range(5)]}

    with patch("jobspy_service.app.main.scrape_jobs", return_value=sample):
        run = main.ingest_board("demo")

    assert run.fetched == 3
    assert run.normalized == 3


@pytest.mark.anyio
async def test_run_all_respects_cadence(monkeypatch, client):
    main.INGESTION_RUNS.clear()
    main.BOARD_CONFIG.clear()
    main.BOARD_CONFIG.update(
        {
            "fast": {
                "enabled": True,
                "cadence": "4h",
                "results_wanted_max": 10,
                "hours_old": 24,
                "delay_seconds": 0,
            },
            "slow": {
                "enabled": True,
                "cadence": "daily",
                "results_wanted_max": 10,
                "hours_old": 24,
                "delay_seconds": 0,
            },
        }
    )
    main._LAST_RUN.clear()
    main._LAST_RUN.update({"fast": None, "slow": None})

    current = {"t": 0.0}

    def fake_time() -> float:
        return current["t"]

    with patch("jobspy_service.app.main.scrape_jobs", return_value={"jobs": []}):
        with patch("jobspy_service.app.main.time.time", side_effect=fake_time):
            res1 = await client.post("/ingest/run-all")
            assert len(res1.json()) == 2
            current["t"] = 3 * 3600
            res2 = await client.post("/ingest/run-all")
            assert res2.json() == []
            current["t"] = 5 * 3600
            res3 = await client.post("/ingest/run-all")
            assert [r["board"] for r in res3.json()] == ["fast"]


def test_cadence_persists_across_restart(monkeypatch) -> None:
    class FakeCursor:
        def __init__(self, store: list[dict[str, float]]):
            self.store = store
            self.result: list[tuple[Any, ...]] | None = None

        def __enter__(self) -> "FakeCursor":  # type: ignore[name-defined]
            return self

        def __exit__(self, *exc: object) -> None:  # pragma: no cover
            return None

        def execute(self, query: str, params: tuple | None = None) -> None:
            if "INSERT INTO ingestion_runs" in query:
                run_id, board, fetched, norm, uniq, errs, ts = params or ()
                self.store.append({"board": board, "ts": float(ts)})
                self.result = None
            elif "SELECT board" in query:
                groups: dict[str, float] = {}
                for row in self.store:
                    groups[row["board"]] = max(
                        groups.get(row["board"], 0), row["ts"]
                    )
                self.result = [(b, t) for b, t in groups.items()]
            elif "SELECT EXTRACT" in query:
                board = params[0] if params else ""
                max_ts = None
                for row in self.store:
                    if row["board"] == board and (
                        max_ts is None or row["ts"] > max_ts
                    ):
                        max_ts = row["ts"]
                self.result = [(max_ts,)]

        def fetchall(self) -> list[tuple[str, float | None]]:
            return self.result or []

        def fetchone(self) -> tuple[float | None] | None:
            return self.result[0] if self.result else None

    store: list[dict[str, float]] = []

    class FakeConn:
        def __init__(self, db: list[dict[str, float]]) -> None:
            self.store = db

        def cursor(self) -> FakeCursor:
            return FakeCursor(self.store)

        def __enter__(self) -> "FakeConn":  # type: ignore[name-defined]
            return self

        def __exit__(self, *exc: object) -> None:  # pragma: no cover
            return None

        def close(self) -> None:
            return None

    def connect() -> FakeConn:
        return FakeConn(store)

    monkeypatch.setattr(main, "_pg_connect", connect)
    main.INGESTION_RUNS.clear()
    main.BOARD_CONFIG.clear()
    main.BOARD_CONFIG["demo"] = {
        "enabled": True,
        "cadence": "4h",
        "results_wanted_max": 10,
        "hours_old": 24,
        "delay": 0,
    }
    with patch("jobspy_service.app.main.scrape_jobs", return_value={"jobs": []}):
        main.ingest_board("demo", now=1.0)
    assert not main._due("demo", now=3600)
    main._LAST_RUN.clear()
    main._load_last_runs()
    assert not main._due("demo", now=3600)
    assert main._due("demo", now=5 * 3600)
    main._LAST_RUN.clear()
    main._load_last_runs()
    assert main._due("demo", now=5 * 3600)
