from pathlib import Path
import sys
import pytest
import httpx

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
