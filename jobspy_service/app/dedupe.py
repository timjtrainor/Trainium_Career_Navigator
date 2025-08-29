"""Helpers for deduplicating job postings using semantic similarity.

The default similarity thresholds are tuned separately for large and small
companies. They can be configured via :class:`DedupConfig` or the environment
variables ``BIG_COMPANY_THRESHOLD`` and ``SMALL_COMPANY_THRESHOLD``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence
import hashlib
import os
import re

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

COMPANY_ALIASES: dict[str, str] = {
    "acme inc": "acme",
    "acme incorporated": "acme",
}

_STOP_WORDS = {"and", "the", "a", "an", "of", "for", "with"}


def _stem(word: str) -> str:
    for suffix in ("ing", "ers", "er", "ed", "es", "s"):
        if word.endswith(suffix) and len(word) > len(suffix) + 2:
            return word[: -len(suffix)]
    return word


def _normalize(text: str) -> str:
    text = re.sub(r"[^\w\s]", " ", text.lower())
    words = [_stem(w) for w in text.split() if w and w not in _STOP_WORDS]
    return " ".join(words)


def _canonical_company(name: str | None) -> str:
    base = re.sub(r"[^\w\s]", " ", (name or "").lower()).strip()
    alias = COMPANY_ALIASES.get(base, base)
    return _normalize(alias)


def _hash(job: dict) -> str:
    title = _normalize(job.get("title", ""))
    company = _canonical_company(job.get("company"))
    key = f"{title}|{company}"
    return hashlib.sha1(key.encode()).hexdigest()


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
    seen: set[str] = set()
    for job in jobs:
        job_hash = _hash(job)
        if job_hash in seen:
            continue
        seen.add(job_hash)
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

