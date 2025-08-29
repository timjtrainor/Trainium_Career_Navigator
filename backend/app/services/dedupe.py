from __future__ import annotations

from typing import List
import os
import psycopg2

from ..models.dedupe_review import DedupeReview

AUTO_THRESHOLD = float(os.getenv("DEDUPE_AUTO_THRESHOLD", "0.95"))
REVIEW_THRESHOLD = float(os.getenv("DEDUPE_REVIEW_THRESHOLD", "0.8"))


def _get_conn() -> psycopg2.extensions.connection:
    dsn = os.environ.get("DATABASE_URL")
    if not dsn:
        raise RuntimeError("DATABASE_URL not set")
    return psycopg2.connect(dsn)


def enqueue_review(job_id_1: int, job_id_2: int, similarity: float) -> None:
    if job_id_1 > job_id_2:
        job_id_1, job_id_2 = job_id_2, job_id_1
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO dedupe_review (job_id_1, job_id_2, similarity, status)
            VALUES (%s, %s, %s, 'pending')
            ON CONFLICT (job_id_1, job_id_2) DO UPDATE SET
                similarity = EXCLUDED.similarity,
                status = 'pending',
                reviewed_at = NULL
            """,
            (job_id_1, job_id_2, similarity),
        )
        conn.commit()
        cur.close()
    finally:
        conn.close()


def list_pending() -> List[DedupeReview]:
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, job_id_1, job_id_2, similarity, status, created_at, reviewed_at
            FROM dedupe_review
            WHERE status = 'pending'
            ORDER BY created_at
            """,
        )
        rows = cur.fetchall()
        cur.close()
    finally:
        conn.close()
    return [
        DedupeReview(
            id=r[0],
            job_id_1=r[1],
            job_id_2=r[2],
            similarity=r[3],
            status=r[4],
            created_at=r[5],
            reviewed_at=r[6],
        )
        for r in rows
    ]


def record_decision(review_id: int, decision: str) -> None:
    if decision not in {"approved", "rejected"}:
        raise ValueError("invalid decision")
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE dedupe_review
            SET status = %s, reviewed_at = NOW()
            WHERE id = %s
            """,
            (decision, review_id),
        )
        conn.commit()
        cur.close()
    finally:
        conn.close()


def should_merge(job_id_1: int, job_id_2: int, similarity: float) -> bool:
    if job_id_1 > job_id_2:
        job_id_1, job_id_2 = job_id_2, job_id_1
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT status FROM dedupe_review
            WHERE job_id_1 = %s AND job_id_2 = %s
            """,
            (job_id_1, job_id_2),
        )
        row = cur.fetchone()
        cur.close()
    finally:
        conn.close()
    if row:
        status = row[0]
        return status == 'approved'
    if similarity >= AUTO_THRESHOLD:
        return True
    if similarity >= REVIEW_THRESHOLD:
        enqueue_review(job_id_1, job_id_2, similarity)
    return False
