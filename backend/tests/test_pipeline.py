from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

import pytest

sys.path.append(str(Path(__file__).resolve().parents[2]))

from jobspy_service.app import dedupe as dedupe_module  # type: ignore
from backend.app.services import evaluation as evaluation_service
from backend.app.services import decisions as decisions_service
from backend.app.services import recommendations as rec_service
from backend.app.models.evaluation import PersonaEvaluation


class _MemoryCursor:
    def __init__(self, db: "_MemoryDB") -> None:
        self.db = db
        self.last_result: Any = None

    def execute(self, query: str, params: tuple | list | None = None) -> None:
        params = params or ()
        if "INSERT INTO evaluations" in query:
            job_id, persona, _provider, vote, rationale, _latency = params
            self.db.evals.append(
                {
                    "job_id": job_id,
                    "persona": persona,
                    "vote": bool(vote),
                    "rationale": rationale,
                }
            )
        elif "INSERT INTO decisions" in query:
            job_id, final, confidence, _method = params
            self.db.decisions[job_id] = {
                "final": bool(final),
                "confidence": float(confidence),
            }
        elif "FROM evaluations" in query and "persona = %s" in query:
            job_id, persona = params
            ev = next(
                (
                    (e["vote"], e["rationale"])
                    for e in self.db.evals
                    if e["job_id"] == job_id and e["persona"] == persona
                ),
                None,
            )
            if "vote_bool" in query:
                self.last_result = ev
            else:
                self.last_result = (ev[1],) if ev else None
        elif "FROM evaluations" in query:
            job_id = params[0]
            personas = params[1:]
            rows = [
                (e["vote"],)
                for e in self.db.evals
                if e["job_id"] == job_id and e["persona"] in personas
            ]
            self.last_result = rows
        elif "FROM decisions" in query:
            rows = [
                (job_id, d["confidence"])
                for job_id, d in self.db.decisions.items()
                if d["final"]
            ]
            self.last_result = rows
        elif "FROM jobs_normalized" in query:
            job_id = params[0]
            job = self.db.jobs.get(job_id)
            self.last_result = (
                job["title"],
                job["company"],
                job["url"],
            ) if job else None

    def fetchone(self):
        res = self.last_result
        self.last_result = None
        return res

    def fetchall(self):
        res = self.last_result or []
        self.last_result = None
        return res

    def close(self) -> None:  # pragma: no cover - no action
        pass


class _MemoryConn:
    def __init__(self, db: "_MemoryDB") -> None:
        self.db = db

    def cursor(self) -> _MemoryCursor:
        return _MemoryCursor(self.db)

    def commit(self) -> None:  # pragma: no cover - no action
        pass

    def close(self) -> None:  # pragma: no cover - no action
        pass


class _MemoryDB:
    def __init__(self) -> None:
        self.evals: list[dict] = []
        self.decisions: dict[str, dict[str, float | bool]] = {}
        self.jobs: dict[str, dict[str, str]] = {}

    def connect(self) -> _MemoryConn:
        return _MemoryConn(self)


def _fake_eval_job(job_id: str) -> list[PersonaEvaluation]:
    conn = evaluation_service._get_conn()
    cur = conn.cursor()
    results: list[PersonaEvaluation] = []
    for persona in evaluation_service.MOTIVATIONAL_PERSONAS:
        vote = job_id == "job1"
        rationale = f"{persona} {'likes' if vote else 'dislikes'}"
        cur.execute(
            "INSERT INTO evaluations VALUES (%s,%s,%s,%s,%s,%s)",
            (job_id, persona, "mock", vote, rationale, 0),
        )
        results.append(PersonaEvaluation(persona=persona, vote_bool=vote, rationale_text=rationale))
    conn.commit()
    cur.close()
    return results


def _fake_eval_decision(job_id: str) -> list[PersonaEvaluation]:
    conn = evaluation_service._get_conn()
    cur = conn.cursor()
    personas = evaluation_service.DECISION_PERSONAS
    results: list[PersonaEvaluation] = []
    for persona in personas:
        vote = job_id == "job1"
        cur.execute(
            "INSERT INTO evaluations VALUES (%s,%s,%s,%s,%s,%s)",
            (job_id, persona, "mock", vote, persona, 0),
        )
        results.append(PersonaEvaluation(persona=persona, vote_bool=vote, rationale_text=persona))
    conn.commit()
    cur.close()
    return results


def test_pipeline_e2e(monkeypatch) -> None:
    # Load deterministic dataset
    data_path = Path(__file__).resolve().parent / "data" / "jobs.json"
    jobs = json.loads(data_path.read_text())

    def fake_embed(job: dict) -> list[float]:
        title = job["title"]
        return [1.0, 0.0] if "Widget" in title else [0.0, 1.0]

    monkeypatch.setattr(dedupe_module, "_embed", fake_embed)

    # Deduplicate using JobSpy helper
    deduped = dedupe_module.dedupe_jobs(jobs)
    assert {j["id"] for j in deduped} == {"job1", "job2"}

    # In-memory DB setup
    memdb = _MemoryDB()
    for job in deduped:
        memdb.jobs[job["id"]] = {
            "title": job["title"],
            "company": job["company"],
            "url": job["url"],
        }

    # Patch database connections and evaluation functions
    monkeypatch.setattr(evaluation_service, "_get_conn", memdb.connect)
    monkeypatch.setattr(decisions_service, "_get_conn", memdb.connect)
    monkeypatch.setattr(rec_service, "_get_conn", memdb.connect)
    monkeypatch.setattr(evaluation_service, "evaluate_job", _fake_eval_job)
    monkeypatch.setattr(evaluation_service, "evaluate_decision_personas", _fake_eval_decision)
    monkeypatch.setattr(decisions_service, "evaluate_decision_personas", _fake_eval_decision)

    # Run evaluations and decisions
    for job in deduped:
        evaluation_service.evaluate_job(job["id"])
        decisions_service.aggregate_decision(job["id"])

    # Recommendations should only include job1
    recs = rec_service.list_recommendations()
    assert [r.job_id for r in recs] == ["job1"]
