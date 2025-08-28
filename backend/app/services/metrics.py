from __future__ import annotations

from datetime import datetime
from typing import List, Optional

import os

import psycopg2

from ..models.metric import Metric


def _get_conn() -> psycopg2.extensions.connection:
    dsn = os.environ.get("DATABASE_URL")
    if not dsn:
        raise RuntimeError("DATABASE_URL not set")
    return psycopg2.connect(dsn)


def log_metric(response_time_ms: float, error_category: Optional[str] = None) -> None:
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO metrics (ts, response_time_ms, error_category)
            VALUES (%s, %s, %s)
            """,
            (datetime.utcnow(), response_time_ms, error_category),
        )
        conn.commit()
        cur.close()
    finally:
        conn.close()


def get_error_rate(days: int = 7) -> float:
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT
                COUNT(*) FILTER (WHERE error_category IS NOT NULL) AS failures,
                COUNT(*) AS total
            FROM metrics
            WHERE ts >= NOW() - INTERVAL %s
            """,
            (f"{days} days",),
        )
        failures, total = cur.fetchone()
        cur.close()
    finally:
        conn.close()
    return 0.0 if total == 0 else failures / total * 100


def get_metrics(days: int = 7) -> List[Metric]:
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT ts, response_time_ms, error_category
            FROM metrics
            WHERE ts >= NOW() - INTERVAL %s
            ORDER BY ts DESC
            """,
            (f"{days} days",),
        )
        rows = cur.fetchall()
        cur.close()
    finally:
        conn.close()
    return [
        Metric(ts=ts, response_time_ms=rt, error_category=cat)
        for ts, rt, cat in rows
    ]


def log_surfaced_job(job_id: str, user_id: str, agent_id: str) -> None:
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO surfaced_jobs (job_id, user_id, agent_id, ts)
            VALUES (%s, %s, %s, NOW())
            """,
            (job_id, user_id, agent_id),
        )
        conn.commit()
        cur.close()
    finally:
        conn.close()


def get_fit_accuracy(days: int = 7) -> float:
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT
                SUM(CASE WHEN vote THEN 1 ELSE 0 END) AS positives,
                COUNT(*) AS total
            FROM feedback
            WHERE ts >= NOW() - INTERVAL %s
            """,
            (f"{days} days",),
        )
        positives, total = cur.fetchone()
        cur.close()
    finally:
        conn.close()
    return 0.0 if total == 0 else positives / total


def count_false_positives(days: int = 7) -> int:
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT COUNT(*)
            FROM surfaced_jobs sj
            LEFT JOIN feedback f ON (
                sj.job_id = f.job_id AND
                sj.user_id = f.user_id AND
                sj.agent_id = f.agent_id
            )
            WHERE sj.ts >= NOW() - INTERVAL %s
              AND (f.vote = FALSE OR f.job_id IS NULL)
            """,
            (f"{days} days",),
        )
        count = cur.fetchone()[0]
        cur.close()
    finally:
        conn.close()
    return count
