from __future__ import annotations

import time
from typing import Optional

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from ..services.metrics import log_metric


class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware to log latency and error category for each request."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            duration_ms = (time.perf_counter() - start) * 1000
            log_metric(duration_ms, "system")
            raise
        duration_ms = (time.perf_counter() - start) * 1000
        category: Optional[str] = None
        status = response.status_code
        if status == 422:
            category = "model"
        elif 400 <= status < 500:
            category = "data"
        elif status >= 500:
            category = "system"
        log_metric(duration_ms, category)
        return response
