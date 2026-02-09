from unittest.mock import AsyncMock, patch

import pytest

from schemas import STaskResponseGet

pytestmark = pytest.mark.anyio


class TestShortenUrl:
    """Тесты для POST /api/v1/shorten."""

    async def test_shorten_url_success(self, async_client):
        """Успешное создание короткой ссылки."""
        with patch("router.TaskRepository") as mock_repo:
            mock_repo.add_one = AsyncMock(return_value="abc123")

            response = await async_client.post(
                "/api/v1/shorten", params={"url": "https://google.com"}
            )

            assert response.status_code == 200
            data = response.json()
            assert data["ok"] is True
            assert data["task_short_link"] == "abc123"

    async def test_shorten_url_without_url(self, async_client):
        """Ошибка при отсутствии url."""
        response = await async_client.post("/api/v1/shorten")

        assert response.status_code == 422


class TestGetHome:
    """Тесты для GET /api/v1/home."""

    async def test_get_home_empty(self, async_client):
        """Получение пустого списка ссылок."""
        with patch("router.TaskRepository") as mock_repo:
            mock_repo.get_all = AsyncMock(return_value=[])

            response = await async_client.get("/api/v1/home")

            assert response.status_code == 200
            assert response.json() == []

    async def test_get_home_with_tasks(self, async_client, mock_task):
        """Получение списка с задачами."""
        with patch("router.TaskRepository") as mock_repo:
            mock_repo.get_all = AsyncMock(return_value=[mock_task])

            response = await async_client.get("/api/v1/home")

            assert response.status_code == 200
            data = response.json()
            assert len(data) == 1
            assert data[0]["url"] == "https://google.com"
            assert data[0]["short_link"] == "abc123"


class TestRedirect:
    """Тесты для GET /{short_link} (редирект)."""

    async def test_redirect_success(self, async_client, mock_task_response_get):
        """Успешный редирект."""
        with patch("router.TaskRepository") as mock_repo:
            mock_repo.get_by_short_link = AsyncMock(return_value=mock_task_response_get)

            response = await async_client.get("/abc123", follow_redirects=False)

            assert response.status_code == 307
            assert response.headers["location"] == "https://google.com"

    async def test_redirect_not_found(self, async_client):
        """Ссылка не найдена."""
        with patch("router.TaskRepository") as mock_repo:
            mock_repo.get_by_short_link = AsyncMock(return_value=None)

            response = await async_client.get("/notexist")

            assert response.status_code == 404
            assert response.json()["detail"] == "Task not found"

    async def test_redirect_adds_https(self, async_client):
        """Добавление https:// если отсутствует."""
        mock_response = STaskResponseGet(
            url="google.com",  # без http
            short_link="abc123",
        )
        with patch("router.TaskRepository") as mock_repo:
            mock_repo.get_by_short_link = AsyncMock(return_value=mock_response)

            response = await async_client.get("/abc123", follow_redirects=False)

            assert response.status_code == 307
            assert response.headers["location"] == "https://google.com"
