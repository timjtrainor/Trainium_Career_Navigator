
import pytest
from unittest.mock import patch, MagicMock
from app.services.extraction import extract_job_details, JobExtract
from app.models.job import JobCreate

@patch("app.services.extraction.OpenAI")
def test_extract_job_details_success(mock_openai):
    # Mock the OpenAI response
    mock_client = MagicMock()
    mock_openai.return_value = mock_client

    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content='{"title": "Software Engineer", "company": "TechCorp", "url": "http://example.com/job", "location": "Remote", "salary_min": 100000, "salary_max": 150000, "job_type": "Full-time"}'))
    ]
    mock_client.chat.completions.create.return_value = mock_response

    text = "We are hiring a Software Engineer at TechCorp. Remote. Salary $100k-$150k. Apply at http://example.com/job"
    result = extract_job_details(text)

    assert result.title == "Software Engineer"
    assert result.company == "TechCorp"
    assert result.url == "http://example.com/job"
    assert result.salary_min == 100000
    assert result.salary_max == 150000
    assert result.job_type == "Full-time"

@patch("app.services.extraction.OpenAI")
def test_extract_job_details_empty_response(mock_openai):
    mock_client = MagicMock()
    mock_openai.return_value = mock_client

    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content='{}'))
    ]
    mock_client.chat.completions.create.return_value = mock_response

    text = "Some random text"
    result = extract_job_details(text)

    # Should return empty fields but not fail
    assert result.title is None

@patch("app.services.extraction.OpenAI")
def test_extract_job_details_invalid_json(mock_openai):
    mock_client = MagicMock()
    mock_openai.return_value = mock_client

    mock_response = MagicMock()
    # Simulate partial json or plain text (though prompt asks for JSON)
    mock_response.choices = [
        MagicMock(message=MagicMock(content='Not JSON'))
    ]
    mock_client.chat.completions.create.return_value = mock_response

    with pytest.raises(Exception):
        extract_job_details("text")
