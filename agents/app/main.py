from pathlib import Path
from typing import Any, Tuple

import psycopg2
from psycopg2.extensions import cursor as PGCursor
import yaml
from fastapi import FastAPI
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel
from pymongo import MongoClient

from .config import settings

app = FastAPI(title="Trainium Agents API", version="0.1.0")


class FeedbackIn(BaseModel):
    persona: str
    input: str
    output: str
    feedback: str


class AgentRequest(BaseModel):
    input: str


@app.get("/health", response_class=JSONResponse)
def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "environment": settings.environment,
        "services": {
            "postgres": {
                "host": settings.pg_host,
                "port": settings.pg_port,
            },
            "mongo": {
                "host": settings.mongo_host,
                "port": settings.mongo_port,
            },
        },
        "llm_providers": {
            "openai": bool(settings.openai_api_key),
            "anthropic": bool(settings.anthropic_api_key),
            "gemini": bool(settings.google_api_key),
        },
        "via": "FastAPI behind Kong",
    }


def _check_postgres() -> Tuple[bool, str | None]:
    try:
        conn = psycopg2.connect(
            host=settings.pg_host,
            port=settings.pg_port,
            user=settings.pg_user,
            password=settings.pg_pass,
            dbname=settings.pg_db,
            connect_timeout=2,
        )
        conn.close()
        return True, None
    except Exception as exc:  # pragma: no cover - network dependent
        return False, str(exc)


def _check_mongo() -> Tuple[bool, str | None]:
    try:
        client = MongoClient(
            host=settings.mongo_host,
            port=settings.mongo_port,
            serverSelectionTimeoutMS=2000,
        )
        client.admin.command("ping")
        client.close()
        return True, None
    except Exception as exc:  # pragma: no cover - network dependent
        return False, str(exc)


def _pg_connect() -> psycopg2.extensions.connection:
    return psycopg2.connect(
        host=settings.pg_host,
        port=settings.pg_port,
        user=settings.pg_user,
        password=settings.pg_pass,
        dbname=settings.pg_db,
    )


@app.get("/personas", response_class=JSONResponse)
def list_personas() -> list[dict[str, Any]]:
    """Expose the personas catalog for the frontend."""
    cfg = Path(__file__).with_name("personas.yml")
    data: dict[str, Any] = {}
    if cfg.exists():
        with cfg.open("r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
    return data.get("personas", [])


@app.post("/agent/{persona}", response_class=JSONResponse)
def invoke_agent(persona: str, body: AgentRequest) -> dict[str, str]:
    """Echo the input for smoke testing purposes."""
    return {"persona": persona, "output": body.input}


@app.post("/feedback", response_class=JSONResponse)
def create_feedback(item: FeedbackIn) -> dict[str, Any]:
    conn = _pg_connect()
    with conn:
        with conn.cursor() as cur:
            _ensure_feedback_table(cur)
            cur.execute(
                "INSERT INTO feedback (persona, input, output, feedback) "
                "VALUES (%s, %s, %s, %s) RETURNING id, created_at",
                (item.persona, item.input, item.output, item.feedback),
            )
            fid, created = cur.fetchone()
    conn.close()
    return {"id": fid, "created_at": created.isoformat()}


@app.get("/feedback", response_class=JSONResponse)
def list_feedback() -> list[dict[str, Any]]:
    conn = _pg_connect()
    with conn:
        with conn.cursor() as cur:
            _ensure_feedback_table(cur)
            cur.execute(
                "SELECT id, persona, input, output, feedback, created_at "
                "FROM feedback ORDER BY id"
            )
            rows = cur.fetchall()
    conn.close()
    return [
        {
            "id": r[0],
            "persona": r[1],
            "input": r[2],
            "output": r[3],
            "feedback": r[4],
            "created_at": r[5].isoformat(),
        }
        for r in rows
    ]


def _ensure_feedback_table(cur: PGCursor) -> None:
    cur.execute(
        "CREATE TABLE IF NOT EXISTS feedback ("
        "id SERIAL PRIMARY KEY, "
        "persona TEXT NOT NULL, "
        "input TEXT NOT NULL, "
        "output TEXT NOT NULL, "
        "feedback TEXT NOT NULL, "
        "created_at TIMESTAMPTZ NOT NULL DEFAULT NOW())",
    )


@app.get("/health/postgres", response_class=JSONResponse)
def health_postgres() -> dict[str, Any]:
    ok, err = _check_postgres()
    resp: dict[str, Any] = {
        "status": "ok" if ok else "error",
        "service": "postgres",
        "host": settings.pg_host,
        "port": settings.pg_port,
    }
    if err:
        resp["error"] = err
    return resp


@app.get("/health/mongo", response_class=JSONResponse)
def health_mongo() -> dict[str, Any]:
    ok, err = _check_mongo()
    resp: dict[str, Any] = {
        "status": "ok" if ok else "error",
        "service": "mongo",
        "host": settings.mongo_host,
        "port": settings.mongo_port,
    }
    if err:
        resp["error"] = err
    return resp


@app.get("/health/db", response_class=JSONResponse)
def health_db() -> dict[str, Any]:
    pg = health_postgres()
    mg = health_mongo()
    status = "ok" if pg["status"] == "ok" and mg["status"] == "ok" else "degraded"
    return {"status": status, "postgres": pg, "mongo": mg}


@app.get("/", response_class=PlainTextResponse)
def root() -> str:
    return "Trainium Agents API. See /health"

