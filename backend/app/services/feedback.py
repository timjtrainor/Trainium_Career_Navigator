from __future__ import annotations

from typing import List, Optional
from datetime import datetime
import os

import psycopg2

from ..models.feedback import Feedback, FeedbackIn
from .metrics import log_surfaced_job


def _get_conn() -> psycopg2.extensions.connection:
    dsn = os.environ.get("DATABASE_URL")
    if not dsn:
        raise RuntimeError("DATABASE_URL not set")
    return psycopg2.connect(dsn)


def save_feedback(fb: FeedbackIn) -> Feedback:
    log_surfaced_job(fb.job_id, fb.user_id, fb.agent_id)
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO feedback (job_id, agent_id, user_id, vote, comment, ts)
            VALUES (%s, %s, %s, %s, %s, NOW())
            RETURNING ts
            """,
            (
                fb.job_id,
                fb.agent_id,
                fb.user_id,
                fb.vote == "up",
                fb.comment,
            ),
        )
        ts = cur.fetchone()[0]
        conn.commit()
        cur.close()
    finally:
        conn.close()
    return Feedback(timestamp=ts, **fb.dict())


def list_feedback(
    job_id: Optional[str] = None,
    agent_id: Optional[str] = None,
    start_ts: Optional[datetime] = None,
    end_ts: Optional[datetime] = None,
) -> List[Feedback]:
    conn = _get_conn()
    try:
        cur = conn.cursor()
        query = "SELECT job_id, agent_id, user_id, vote, comment, ts FROM feedback"
        conditions: List[str] = []
        params: List[object] = []
        if job_id:
            conditions.append("job_id = %s")
            params.append(job_id)
        if agent_id:
            conditions.append("agent_id = %s")
            params.append(agent_id)
        if start_ts:
            conditions.append("ts >= %s")
            params.append(start_ts)
        if end_ts:
            conditions.append("ts <= %s")
            params.append(end_ts)
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += " ORDER BY ts DESC"
        cur.execute(query, tuple(params))
        rows = cur.fetchall()
        cur.close()
    finally:
        conn.close()
    results: List[Feedback] = []
    for j, a, u, v, c, ts in rows:
        vote = "up" if v else "down"
        results.append(
            Feedback(
                job_id=j,
                agent_id=a,
                user_id=u,
                vote=vote,
                comment=c,
                timestamp=ts,
            )
        )
    return results
