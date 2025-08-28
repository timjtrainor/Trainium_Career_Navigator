from pathlib import Path
import sys
from unittest.mock import patch

from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[2]))
from jobspy_service.app.main import app


client = TestClient(app)


def test_disabled_returns_501(monkeypatch):
    monkeypatch.setenv("JOBSPY_ENABLED", "false")
    monkeypatch.setenv("JOBSPY_SOURCES", "google")
    response = client.get(
        "/jobs/search", params={"source": "google", "google_search_term": "python"}
    )
    assert response.status_code == 501
    assert response.json()["detail"] == "scraping disabled"


def test_google_not_allowlisted_returns_403(monkeypatch):
    monkeypatch.setenv("JOBSPY_ENABLED", "true")
    monkeypatch.setenv("JOBSPY_SOURCES", "indeed,linkedin")
    response = client.get(
        "/jobs/search", params={"source": "google", "google_search_term": "python"}
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Google not allowlisted"


def test_google_missing_search_term_returns_400(monkeypatch):
    monkeypatch.setenv("JOBSPY_ENABLED", "true")
    monkeypatch.setenv("JOBSPY_SOURCES", "google")
    response = client.get("/jobs/search", params={"source": "google"})
    assert response.status_code == 400
    assert response.json()["detail"] == "google_search_term required for Google Jobs"


def test_google_scrape_with_delay(monkeypatch):
    calls = []

    def fake_sleep(delay: float) -> None:
        calls.append(("sleep", delay))

    def fake_scrape(source: str, *, search_term: str | None = None):
        calls.append(("scrape", source, search_term))
        return {"jobs": [], "source": source}

    monkeypatch.setenv("JOBSPY_ENABLED", "true")
    monkeypatch.setenv("JOBSPY_SOURCES", "google")
    monkeypatch.setenv("JOBSPY_DELAY_SECONDS", "2")

    with patch("jobspy_service.app.main.time.sleep", side_effect=fake_sleep) as mock_sleep:
        with patch(
            "jobspy_service.app.main.scrape_jobs", side_effect=fake_scrape
        ) as mock_scrape:
            response = client.get(
                "/jobs/search",
                params={"source": "google", "google_search_term": "python"},
            )

    assert calls[0][0] == "sleep"
    assert calls[1][0] == "scrape"
    assert calls[0][1] == 2
    assert calls[1][1:] == ("google", "python")
    mock_sleep.assert_called_once_with(2)
    mock_scrape.assert_called_once_with("google", search_term="python")
    assert response.status_code == 200
    body = response.json()
    assert body["source"] == "google"
    assert "jobs" in body


def test_normalizes_output_for_multiple_sources(monkeypatch):
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

    def fake_scrape(source: str, *, search_term: str | None = None):
        return {"jobs": raw_jobs[source], "source": source}

    for src in ("indeed", "linkedin"):
        with patch("jobspy_service.app.main.scrape_jobs", side_effect=fake_scrape):
            response = client.get("/jobs/search", params={"source": src})
        assert response.status_code == 200
        job = response.json()["jobs"][0]
        assert set(job) == {
            "title",
            "company",
            "description",
            "location",
            "url",
            "remote_status",
        }

        if src == "indeed":
            assert job["title"] == "Engineer"
            assert job["company"] == "Acme"
            assert job["location"] == "NY"
            assert job["remote_status"] == "remote"
        else:
            assert job["title"] == "Developer"
            assert job["company"] == "Beta"
            assert job["location"] == "SF"
            assert job["remote_status"] == "remote"

