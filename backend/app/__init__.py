from __future__ import annotations

from fastapi import FastAPI

from .middleware.metrics import MetricsMiddleware
from .routes.metrics import router as metrics_router
from .routes.personas import router as personas_router


def create_app() -> FastAPI:
    """Create and configure a FastAPI application."""
    app = FastAPI()
    app.add_middleware(MetricsMiddleware)
    app.include_router(personas_router)
    app.include_router(metrics_router)
    return app
