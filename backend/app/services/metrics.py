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
