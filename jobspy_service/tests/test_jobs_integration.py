from pathlib import Path
import sys
import time
from unittest.mock import patch

import pytest

sys.path.append(str(Path(__file__).resolve().parents[2]))
from jobspy_service.app.main import JobSearchResponse  # noqa: E402
import jobspy_service.app.main as main  # noqa: E402


@pytest.mark.anyio
async def test_search_returns_schema_for_multiple_sources(monkeypatch, client):
    """Endpoint returns data conforming to schema for each source."""
    monkeypatch.setenv("JOBSPY_ENABLED", "true")
    monkeypatch.setenv("JOBSPY_SOURCES", "indeed,linkedin")

    raw_jobs = {
        "indeed": [
            {
                "job_title": "Engineer",
                "company": "Acme",
                "job_description": "Build stuff",
                "city": "NY",
                "job_url": "http://indeed/job1",
                "is_remote": True,
            }
        ],
        "linkedin": [
            {
                "title": "Developer",
                "company_name": "Beta",
                "description": "Write code",
                "location": "SF",
                "url": "http://linkedin/job2",
                "remote": "remote",
            }
        ],
    }

    def fake_scrape(
        source: str,
        *,
        search_term: str | None = None,
        results_wanted_max: int | None = None,
    ) -> dict[str, object]:
        return {"jobs": raw_jobs[source], "source": source}

    for src in ("indeed", "linkedin"):
        with patch("jobspy_service.app.main.scrape_jobs", side_effect=fake_scrape):
            response = await client.get("/jobs/search", params={"source": src})
        assert response.status_code == 200
        data = JobSearchResponse.model_validate(response.json())
        assert data.source == src
        assert len(data.jobs) == 1
        job = data.jobs[0]
        assert set(job.model_dump()) == {
            "title",
            "company",
            "description",
            "location",
            "url",
            "remote_status",
        }


@pytest.mark.anyio
async def test_cached_query_returns_under_one_second(monkeypatch, client):
    """Second identical query should be served from cache quickly."""
    main._CACHE.clear()
    monkeypatch.setenv("JOBSPY_ENABLED", "true")
    monkeypatch.setenv("JOBSPY_SOURCES", "indeed")
    monkeypatch.setenv("JOBSPY_DELAY_SECONDS", "1")

    calls = []

    def fake_scrape(
        source: str,
        *,
        search_term: str | None = None,
        results_wanted_max: int | None = None,
    ) -> dict[str, object]:
        calls.append("scrape")
        return {"jobs": [], "source": source}

    with patch("jobspy_service.app.main.scrape_jobs", side_effect=fake_scrape):
        start = time.perf_counter()
        first = await client.get("/jobs/search", params={"source": "indeed"})
        first_duration = time.perf_counter() - start

        start = time.perf_counter()
        second = await client.get("/jobs/search", params={"source": "indeed"})
        second_duration = time.perf_counter() - start

    assert first.status_code == 200
    assert second.status_code == 200
    assert calls == ["scrape"]
    assert second_duration < 1.0
    main._CACHE.clear()
