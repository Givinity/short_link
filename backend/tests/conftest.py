from datetime import datetime
from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from app import app
from schemas import STask, STaskResponseGet


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def async_client():
    """Асинхронный HTTP клиент для тестирования API."""
    with patch("app.init_redis", new=AsyncMock()):
        with patch("app.close_redis", new=AsyncMock()):
            transport = ASGITransport(app=app)
            async with AsyncClient(
                transport=transport, base_url="http://test"
            ) as client:
                yield client


@pytest.fixture
def mock_task_response_get():
    """Мок ответа get_by_short_link."""
    return STaskResponseGet(url="https://google.com", short_link="abc123")


@pytest.fixture
def mock_task():
    """Мок полной задачи."""
    return STask(
        id=1,
        url="https://google.com",
        short_link="abc123",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        is_active=True,
        is_deleted=False,
    )


@pytest.fixture
def mock_repository():
    """Мок репозитория."""
    with patch("api.routers.tasks.task_service") as mock_tasks:
        mock_tasks.shorten = AsyncMock(return_value="abc123")
        mock_tasks.get_all = AsyncMock(return_value=[])
        with patch("api.routers.redirect.task_service") as mock_redirect:
            mock_redirect.get_by_short_link = AsyncMock(return_value=None)
            yield mock_tasks
