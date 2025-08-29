from __future__ import annotations

from typing import List

from .evaluation import _get_conn
from ..models.recommendation import Recommendation


def list_recommendations() -> List[Recommendation]:
    """Return recommended jobs with positive final decisions."""
    conn = _get_conn()
    results: List[Recommendation] = []
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT job_unique_id, confidence FROM decisions "
            "WHERE final_decision_bool = TRUE"
        )
        decisions = cur.fetchall()
        for job_id, confidence in decisions:
            cur.execute(
                "SELECT title, company, url FROM jobs_normalized "
                "WHERE job_id_ext = %s",
                (job_id,),
            )
            job_row = cur.fetchone()
            title, company, url = job_row if job_row else (None, None, None)
            cur.execute(
                "SELECT rationale_text FROM evaluations "
                "WHERE job_unique_id = %s AND persona = %s",
                (job_id, "judge"),
            )
            rationale_row = cur.fetchone()
            rationale = rationale_row[0] if rationale_row else None
            results.append(
                Recommendation(
                    job_id=job_id,
                    title=title,
                    company=company,
                    url=url,
                    rationale=rationale,
                    confidence=confidence,
                )
            )
        cur.close()
    finally:
        conn.close()
    return results
