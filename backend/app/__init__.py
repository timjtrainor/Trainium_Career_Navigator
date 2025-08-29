from __future__ import annotations

from fastapi import FastAPI

from .middleware.metrics import MetricsMiddleware
from .routes.metrics import router as metrics_router
from .routes.personas import router as personas_router
from .routes.feedback import router as feedback_router
from .routes.dedupe import router as dedupe_router


def create_app() -> FastAPI:
    """Create and configure a FastAPI application."""
    app = FastAPI()
    app.add_middleware(MetricsMiddleware)
    app.include_router(personas_router)
    app.include_router(metrics_router)
    app.include_router(feedback_router)
    app.include_router(dedupe_router)
    return app
