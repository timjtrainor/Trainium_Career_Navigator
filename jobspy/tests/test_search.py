from pathlib import Path
import sys
from fastapi.testclient import TestClient
from unittest.mock import patch

sys.path.append(str(Path(__file__).resolve().parents[2]))
from jobspy.app.main import app


client = TestClient(app)


def test_linkedin_allowed_when_allowlisted():
    response = client.get("/jobs/search", params={"source": "linkedin", "allowlist": "linkedin"})
    assert response.status_code == 200


def test_source_not_allowlisted_rejected():
    response = client.get("/jobs/search", params={"source": "linkedin", "allowlist": "indeed"})
    assert response.status_code == 400


@patch("jobspy.app.main.scrape_jobs", return_value={"jobs": []})
@patch("jobspy.app.main.time.sleep")
def test_delay_before_scrape(mock_sleep, mock_scrape, monkeypatch):
    monkeypatch.setenv("JOBSPY_DELAY_SECONDS", "2")
    client.get("/jobs/search", params={"source": "linkedin", "allowlist": "linkedin"})
    mock_sleep.assert_called_once_with(2.0)
    mock_scrape.assert_called_once()

