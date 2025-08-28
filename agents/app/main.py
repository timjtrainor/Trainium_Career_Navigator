from fastapi import FastAPI
from fastapi.responses import JSONResponse, PlainTextResponse
import os

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

@app.get("/", response_class=PlainTextResponse)
def root():
    return "Trainium Agents API. See /health"