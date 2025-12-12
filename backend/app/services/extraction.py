from __future__ import annotations

import json
import logging
import os
from typing import Optional

from openai import OpenAI
from pydantic import BaseModel, Field

from ..models.job import JobCreate

logger = logging.getLogger(__name__)

class JobExtract(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    url: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    job_type: Optional[str] = None

def extract_job_details(text: str) -> JobExtract:
    """
    Extracts job details from raw text using OpenAI.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY is not set.")
        # Return empty extraction if no key (or raise error)
        # Raising error is better so frontend knows it failed
        raise ValueError("OpenAI API key not configured.")

    client = OpenAI(api_key=api_key)

    prompt = (
        "You are an expert at parsing job descriptions. "
        "Extract the following information from the text provided:\n"
        "- Job Title\n"
        "- Company Name\n"
        "- Job Posting URL (if present)\n"
        "- Location\n"
        "- Full Job Description (summary or full text if reasonable)\n"
        "- Minimum Salary (integer, yearly)\n"
        "- Maximum Salary (integer, yearly)\n"
        "- Job Type (Full-time, Part-time, Contract, Internship, Freelance)\n\n"
        "Return the output as a valid JSON object with keys: "
        "title, company, url, location, description, salary_min, salary_max, job_type.\n"
        "If a field cannot be found, set it to null.\n"
        "For salaries, convert to yearly integers. If hourly, multiply by 2080.\n\n"
        f"TEXT:\n{text}"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", # or gpt-3.5-turbo, gpt-4o-mini is cost effective and good
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts structured data from job descriptions."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.1,
        )

        content = response.choices[0].message.content
        if not content:
            return JobExtract()

        data = json.loads(content)

        return JobExtract(
            title=data.get("title"),
            company=data.get("company"),
            url=data.get("url"),
            location=data.get("location"),
            description=data.get("description"),
            salary_min=data.get("salary_min"),
            salary_max=data.get("salary_max"),
            job_type=data.get("job_type"),
        )

    except Exception as e:
        logger.exception("Failed to extract job details")
        raise e
