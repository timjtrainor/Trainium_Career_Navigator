from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import List

import yaml

from ..models.persona import Persona


@lru_cache
def load_personas() -> List[Persona]:
    """Load persona definitions from YAML and cache the result."""
    config_path = Path(__file__).resolve().parents[2] / "config" / "personas.yml"
    with config_path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    return [Persona(**p) for p in data.get("personas", [])]
