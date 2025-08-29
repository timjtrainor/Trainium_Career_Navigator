"""Tests for the job deduplication helpers."""

from __future__ import annotations

from typing import Any

import numpy as np

from jobspy_service.app import dedupe
from jobspy_service.app.dedupe import DedupConfig, dedupe_jobs


def test_semantic_duplicates_merge(monkeypatch: Any) -> None:
    """Jobs with very similar content are collapsed."""

    embeddings = {
        "Python Developer": np.array([1.0, 0.0]),
        "Backend Engineer": np.array([1.0, 0.0]),
        "Graphic Designer": np.array([0.0, 1.0]),
    }

    def fake_embed(job: dict) -> np.ndarray:
        return embeddings[job["title"]]

    monkeypatch.setattr(dedupe, "_embed", fake_embed)

    jobs = [
        {"title": "Python Developer", "description": "Build backend APIs"},
        {
            "title": "Backend Engineer",
            "description": "Develop APIs using Python",
        },
        {
            "title": "Graphic Designer",
            "description": "Create visual assets",
        },
    ]

    deduped = dedupe_jobs(jobs)
    assert len(deduped) == 2
    titles = {j["title"] for j in deduped}
    assert "Graphic Designer" in titles
    assert ("Python Developer" in titles) ^ ("Backend Engineer" in titles)


def test_thresholds_config_override(monkeypatch: Any) -> None:
    """Custom thresholds allow different behaviour per company size."""

    embeddings = {
        "A": np.array([1.0, 0.0]),
        "B": np.array([0.8, 0.6]),  # cosine with A -> 0.8
        "C": np.array([0.0, 1.0]),
        "D": np.array([0.6, 0.8]),  # cosine with C -> 0.8
    }

    def fake_embed(job: dict) -> np.ndarray:
        return embeddings[job["title"]]

    monkeypatch.setattr(dedupe, "_embed", fake_embed)

    jobs = [
        {"title": "A", "description": "", "company_size": "big"},
        {"title": "B", "description": "", "company_size": "big"},
        {"title": "C", "description": "", "company_size": "small"},
        {"title": "D", "description": "", "company_size": "small"},
    ]

    config = DedupConfig(big_company_threshold=0.75, small_company_threshold=0.85)
    deduped = dedupe_jobs(jobs, config=config)

    assert {j["title"] for j in deduped} == {"A", "C", "D"}


def test_company_alias_collapse(monkeypatch: Any) -> None:
    """Company name variants map to a single canonical record."""

    embeddings = {
        "Acme Inc.": np.array([1.0, 0.0]),
        "Acme Incorporated": np.array([0.0, 1.0]),
    }

    def fake_embed(job: dict) -> np.ndarray:
        return embeddings[job["company"]]

    monkeypatch.setattr(dedupe, "_embed", fake_embed)

    jobs = [
        {
            "title": "Widget Engineer",
            "description": "Build widgets",
            "company": "Acme Inc.",
        },
        {
            "title": "Widget Engineer",
            "description": "Design widgets",
            "company": "Acme Incorporated",
        },
    ]

    deduped = dedupe_jobs(jobs)
    assert len(deduped) == 1

