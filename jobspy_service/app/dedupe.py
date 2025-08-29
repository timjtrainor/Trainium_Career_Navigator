"""Helpers for deduplicating job postings using semantic similarity."""

from __future__ import annotations

from typing import Sequence

import numpy as np
from sentence_transformers import SentenceTransformer


_MODEL = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def _embed(job: dict) -> np.ndarray:
    """Return a normalized embedding for the job title and description."""

    text = " ".join(
        part for part in (job.get("title"), job.get("description")) if part
    )
    return _MODEL.encode(text, normalize_embeddings=True)


def _cosine(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity for normalized vectors."""

    return float(np.dot(a, b))


def dedupe_jobs(jobs: Sequence[dict], *, threshold: float = 0.85) -> list[dict]:
    """Remove semantically similar job postings."""

    kept: list[dict] = []
    embeddings: list[np.ndarray] = []
    for job in jobs:
        emb = _embed(job)
        if all(_cosine(emb, existing) < threshold for existing in embeddings):
            kept.append(job)
            embeddings.append(emb)
    return kept

