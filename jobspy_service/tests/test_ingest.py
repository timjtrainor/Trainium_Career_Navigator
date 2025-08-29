from pathlib import Path
import sys
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
    assert len(main.INGESTION_RUNS) == 1


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
