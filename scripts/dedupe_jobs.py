from __future__ import annotations

from typing import Iterable, List, Tuple

from backend.app.services.dedupe import should_merge


def dedupe_jobs(pairs: Iterable[Tuple[int, int, float]]) -> List[Tuple[int, int]]:
    """Return pairs that should be merged.

    Borderline pairs are queued for manual review and excluded from the result
    until a human decision is recorded.
    """

    merged: List[Tuple[int, int]] = []
    for job_a, job_b, similarity in pairs:
        if should_merge(job_a, job_b, similarity):
            merged.append((job_a, job_b))
    return merged
