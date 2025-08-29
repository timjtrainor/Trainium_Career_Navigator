from __future__ import annotations

import logging

from .evaluation import (
    DECISION_PERSONAS,
    _get_conn,
    evaluate_decision_personas,
)
from ..models.decision import Decision

logger = logging.getLogger(__name__)


def aggregate_decision(job_id: str) -> Decision:
    """Use the Judge persona to record the final decision for a job."""
    evaluate_decision_personas(job_id)
    conn = _get_conn()
    final = False
    confidence = 0.0
    method = "judge"
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT vote_bool, rationale_text FROM evaluations "
            "WHERE job_unique_id = %s AND persona = %s",
            (job_id, "judge"),
        )
        row = cur.fetchone()
        if row:
            final = bool(row[0])
        personas = [p for p in DECISION_PERSONAS if p != "judge"]
        placeholders = ",".join(["%s"] * len(personas))
        cur.execute(
            f"SELECT vote_bool FROM evaluations WHERE job_unique_id = %s "
            f"AND persona IN ({placeholders})",
            [job_id, *personas],
        )
        votes = cur.fetchall()
        yes = sum(1 for (vote,) in votes if vote)
        no = sum(1 for (vote,) in votes if not vote)
        total = yes + no
        confidence = (max(yes, no) / total) if total else 0.0
        cur.execute(
            """
            INSERT INTO decisions (
                job_unique_id, final_decision_bool, confidence, method, created_at
            ) VALUES (%s, %s, %s, %s, NOW())
            ON CONFLICT (job_unique_id) DO UPDATE SET
                final_decision_bool = EXCLUDED.final_decision_bool,
                confidence = EXCLUDED.confidence,
                method = EXCLUDED.method,
                created_at = EXCLUDED.created_at
            """,
            (job_id, final, confidence, method),
        )
        conn.commit()
        cur.close()
    finally:
        conn.close()
    return Decision(
        job_id=job_id,
        final_decision_bool=final,
        confidence=confidence,
        method=method,
    )
