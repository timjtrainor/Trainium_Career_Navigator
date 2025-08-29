from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from .evaluation import _get_conn
from ..models.job import Job, JobDetail, EvaluationSummary


def list_unique_jobs(
    query: str | None = None,
    company: str | None = None,
    source: str | None = None,
    since: datetime | None = None,
    *,
    limit: int = 50,
    offset: int = 0,
) -> List[Job]:
    """Return jobs matching filters ordered by recency."""

    conn = _get_conn()
    results: List[Job] = []
    try:
        cur = conn.cursor()
        clauses: list[str] = []
        params: list[object] = []
        if query:
            clauses.append("(title ILIKE %s OR description ILIKE %s)")
            like = f"%{query}%"
            params.extend([like, like])
        if company:
            clauses.append("company ILIKE %s")
            params.append(f"%{company}%")
        if source:
            clauses.append("source = %s")
            params.append(source)
        if since:
            clauses.append("updated_at >= %s")
            params.append(since)
        sql = (
            "SELECT job_id_ext, title, company, url, source, updated_at "
            "FROM jobs_normalized"
        )
        if clauses:
            sql += " WHERE " + " AND ".join(clauses)
        sql += " ORDER BY updated_at DESC LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        cur.execute(sql, params)
        for row in cur.fetchall():
            results.append(
                Job(
                    job_id=row[0],
                    title=row[1],
                    company=row[2],
                    url=row[3],
                    source=row[4],
                    updated_at=row[5],
                )
            )
        cur.close()
    finally:
        conn.close()
    return results


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
