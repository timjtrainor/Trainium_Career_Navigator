from __future__ import annotations

from datetime import datetime, timedelta
from typing import List, Optional, Tuple
from uuid import uuid4

from .evaluation import _get_conn
from ..models.job import (
    EvaluationSummary,
    Job,
    JobCreate,
    JobCreateResponse,
    JobDetail,
)


def list_unique_jobs(
    query: str | None = None,
    company: str | None = None,
    sources: List[str] | None = None,
    since: str | None = None,
    hide: List[str] | None = None,
    *,
    page: int = 1,
    page_size: int = 50,
) -> Tuple[List[Job], int]:
    """Return jobs matching filters ordered by recency."""

    conn = _get_conn()
    results: List[Job] = []
    total = 0
    try:
        cur = conn.cursor()
        clauses: list[str] = []
        params: list[object] = []
        if query:
            clauses.append("(title ILIKE %s OR company ILIKE %s)")
            like = f"%{query}%"
            params.extend([like, like])
        if company:
            clauses.append("company = %s")
            params.append(company)
        if sources:
            placeholders = ",".join(["%s"] * len(sources))
            clauses.append(f"source IN ({placeholders})")
            params.extend(sources)
        if since:
            now = datetime.utcnow()
            delta = {
                "24h": timedelta(hours=24),
                "7d": timedelta(days=7),
                "30d": timedelta(days=30),
            }.get(since)
            if delta:
                clauses.append("updated_at >= %s")
                params.append(now - delta)
        if hide:
            placeholders = ",".join(["%s"] * len(hide))
            clauses.append(f"COALESCE(decision, 'undecided') NOT IN ({placeholders})")
            params.extend(hide)
        where_sql = " WHERE " + " AND ".join(clauses) if clauses else ""
        base_sql = (
            "FROM jobs_normalized j LEFT JOIN job_status d "
            "ON j.job_id_ext = d.job_id"
        )
        count_sql = f"SELECT COUNT(*) FROM (SELECT DISTINCT ON (company, title) 1 {base_sql}{where_sql}) AS sub"
        cur.execute(count_sql, params)
        total_row = cur.fetchone()
        total = total_row[0] if total_row else 0
        limit = page_size
        offset = (page - 1) * page_size
        list_sql = (
            "SELECT DISTINCT ON (j.company, j.title) j.job_id_ext, j.title, j.company, "
            "j.url, j.source, j.updated_at, COALESCE(d.decision, 'undecided') "
            f"{base_sql}{where_sql} ORDER BY j.company, j.title, j.updated_at DESC "
            "LIMIT %s OFFSET %s"
        )
        cur.execute(list_sql, params + [limit, offset])
        for row in cur.fetchall():
            results.append(
                Job(
                    job_id=row[0],
                    title=row[1],
                    company=row[2],
                    url=row[3],
                    source=row[4],
                    updated_at=row[5],
                    decision=row[6],
                )
            )
        cur.close()
    finally:
        conn.close()
    return results, total


def get_job_detail(job_id: str) -> Optional[JobDetail]:
    """Return a job record with evaluation summary."""

    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT job_id_ext, title, company, description, location, url, "
            "source, updated_at FROM jobs_normalized WHERE job_id_ext = %s",
            (job_id,),
        )
        row = cur.fetchone()
        if not row:
            cur.close()
            return None
        job = Job(
            job_id=row[0],
            title=row[1],
            company=row[2],
            url=row[5],
            source=row[6],
            updated_at=row[7],
        )
        description, location = row[3], row[4]
        cur.execute(
            "SELECT vote_bool, COUNT(*) FROM evaluations "
            "WHERE job_unique_id = %s GROUP BY vote_bool",
            (job_id,),
        )
        counts = {True: 0, False: 0}
        for vote, count in cur.fetchall():
            if vote is None:
                continue
            counts[vote] = count
        cur.execute(
            "SELECT final_decision_bool, confidence FROM decisions "
            "WHERE job_unique_id = %s",
            (job_id,),
        )
        dec_row = cur.fetchone()
        summary = EvaluationSummary(
            yes=counts.get(True, 0),
            no=counts.get(False, 0),
            final_decision_bool=dec_row[0] if dec_row else None,
            confidence=dec_row[1] if dec_row else None,
        )
        cur.close()
    finally:
        conn.close()
    return JobDetail(
        job_id=job.job_id,
        title=job.title,
        company=job.company,
        url=job.url,
        source=job.source,
        updated_at=job.updated_at,
        description=description,
        location=location,
        evaluation=summary,
    )


def create_job(new_job: JobCreate) -> JobCreateResponse:
    """Persist a manually logged job."""

    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT job_id_ext FROM jobs_normalized WHERE title = %s AND company = %s AND url = %s",
            (new_job.title, new_job.company, new_job.url),
        )
        if cur.fetchone():
            raise ValueError("duplicate job")
        job_id = str(uuid4())
        cur.execute(
            """
            INSERT INTO jobs_normalized (
                source, title, company, description, location, url, job_id_ext, updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
            RETURNING updated_at
            """,
            (
                "manual",
                new_job.title,
                new_job.company,
                new_job.description,
                new_job.location,
                new_job.url,
                job_id,
            ),
        )
        created_at = cur.fetchone()[0]
        cur.execute(
            "INSERT INTO job_status (job_id, decision) VALUES (%s, %s)",
            (job_id, "undecided"),
        )
        conn.commit()
        cur.close()
    finally:
        conn.close()
    return JobCreateResponse(job_id=job_id, status="logged", created_at=created_at)
