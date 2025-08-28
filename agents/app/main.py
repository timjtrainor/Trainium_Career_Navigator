from typing import Any, Tuple

from fastapi import FastAPI
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel
from crewai import Agent
import psycopg2
from pymongo import MongoClient

from .config import settings

app = FastAPI(title="Trainium Agents API", version="0.1.0")


class Prompt(BaseModel):
    message: str

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


@app.post("/api/agent/{persona}", response_class=JSONResponse)
def run_agent(persona: str, prompt: Prompt) -> dict[str, str]:
    agent = Agent(role=persona, goal="Echo user input", backstory="Mock agent")
    return {"persona": agent.role, "echo": prompt.message}

@app.get("/", response_class=PlainTextResponse)
def root() -> str:
    return "Trainium Agents API. See /health"
