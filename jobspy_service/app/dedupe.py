"""Helpers for deduplicating job postings using semantic similarity.

The default similarity thresholds are tuned separately for large and small
companies. They can be configured via :class:`DedupConfig` or the environment
variables ``BIG_COMPANY_THRESHOLD`` and ``SMALL_COMPANY_THRESHOLD``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence
import os

import numpy as np

try:  # pragma: no cover - dependency not installed in tests
    from sentence_transformers import SentenceTransformer  # type: ignore
except Exception:  # pragma: no cover - handled gracefully
    SentenceTransformer = None  # type: ignore[assignment]

_MODEL = (
    SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    if SentenceTransformer is not None
    else None
)


@dataclass
class DedupConfig:
    """Configuration for job deduplication.

    Attributes
    ----------
    big_company_threshold:
        Similarity cutoff for postings from large companies. Defaults to ``0.9``.
    small_company_threshold:
        Similarity cutoff for small companies. Defaults to ``0.85``.
    """

    big_company_threshold: float = 0.9
    small_company_threshold: float = 0.85

    @classmethod
    def from_env(cls) -> "DedupConfig":
        """Load thresholds from environment variables if present."""

        return cls(
            big_company_threshold=float(
                os.getenv("BIG_COMPANY_THRESHOLD", cls.big_company_threshold)
            ),
            small_company_threshold=float(
                os.getenv("SMALL_COMPANY_THRESHOLD", cls.small_company_threshold)
            ),
        )


def _embed(job: dict) -> np.ndarray:
    """Return a normalized embedding for the job title and description."""

    if _MODEL is None:  # pragma: no cover - only when dependency missing
        raise RuntimeError("sentence-transformers is required for embedding")
    text = " ".join(
        part for part in (job.get("title"), job.get("description")) if part
    )
    return _MODEL.encode(text, normalize_embeddings=True)


def _cosine(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity for normalized vectors."""

    return float(np.dot(a, b))


def dedupe_jobs(
    jobs: Sequence[dict], *, config: DedupConfig | None = None
) -> list[dict]:
    """Remove semantically similar job postings.

    Parameters
    ----------
    jobs:
        Iterable of job dictionaries.
    config:
        Optional :class:`DedupConfig`. When ``None`` the environment variables
        ``BIG_COMPANY_THRESHOLD`` and ``SMALL_COMPANY_THRESHOLD`` are used.
    """

    cfg = config or DedupConfig.from_env()
    kept: list[dict] = []
    embeddings: list[np.ndarray] = []
    for job in jobs:
        emb = _embed(job)
        threshold = (
            cfg.big_company_threshold
            if job.get("company_size") == "big"
            else cfg.small_company_threshold
        )
        if all(_cosine(emb, existing) < threshold for existing in embeddings):
            kept.append(job)
            embeddings.append(emb)
    return kept

