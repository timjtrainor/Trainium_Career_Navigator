import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse, PlainTextResponse
import psycopg2
from pymongo import MongoClient

from .config import settings

app = FastAPI(title="Trainium Agents API", version="0.1.0")

@app.get("/health", response_class=JSONResponse)
def health():
    return {
        "status": "ok",
        "environment": settings.environment,
        "services": {
            "postgres": {"host": settings.pg_host, "port": settings.pg_port},
            "mongo": {"host": settings.mongo_host, "port": settings.mongo_port},
        },
        "llm_providers": {
            "openai": bool(settings.openai_api_key),
            "anthropic": bool(settings.anthropic_api_key),
            "gemini": bool(settings.google_api_key),
        },
        "via": "FastAPI behind Kong",
    }


# Health check endpoint for DBs
@app.get("/health/db", response_class=JSONResponse)
def health_db():
    errors = {}
    # Check Postgres
    try:
        conn = psycopg2.connect(
            host=settings.pg_host,
            port=settings.pg_port,
            user=settings.pg_user,
            password=settings.pg_password,
            dbname=settings.pg_db,
            connect_timeout=2
        )
        conn.close()
        pg_status = True
    except Exception as e:
        errors['postgres'] = str(e)
        pg_status = False
    # Check Mongo
    try:
        mongo_uri = f"mongodb://{settings.mongo_user}:{settings.mongo_password}@{settings.mongo_host}:{settings.mongo_port}"
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=2000)
        # The following will force a connection call
        client.admin.command('ping')
        client.close()
        mongo_status = True
    except Exception as e:
        errors['mongo'] = str(e)
        mongo_status = False
    if pg_status and mongo_status:
        status_str = "ok"
    else:
        status_str = "degraded"
    resp = {"status": status_str}
    if errors:
        resp["errors"] = errors
    return resp

@app.get("/", response_class=PlainTextResponse)
def root():
    return "Trainium Agents API. See /health"