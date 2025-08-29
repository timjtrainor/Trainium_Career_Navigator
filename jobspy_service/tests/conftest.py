from pathlib import Path
import sys
import types
import pytest
import httpx

# Minimal numpy stub for tests
numpy_stub = types.ModuleType("numpy")
numpy_stub.array = lambda seq: list(seq)
numpy_stub.dot = lambda a, b: sum(x * y for x, y in zip(a, b))
numpy_stub.ndarray = list  # type: ignore[attr-defined]
sys.modules.setdefault("numpy", numpy_stub)

sys.path.append(str(Path(__file__).resolve().parents[2]))
from jobspy_service.app.main import app  # noqa: E402


@pytest.fixture
async def client():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"
