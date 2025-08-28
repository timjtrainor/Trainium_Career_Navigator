from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel


class Metric(BaseModel):
    """Represents a logged request metric."""

    ts: datetime
    response_time_ms: float
    error_category: Optional[Literal["system", "data", "model"]] = None
