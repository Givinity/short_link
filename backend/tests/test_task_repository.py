from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from repositories.task import TaskRepository

pytestmark = pytest.mark.anyio


class TestTaskRepositoryFindByShortLink:
    async def test_get_by_short_link_found(self):
        mock_session = AsyncMock()
        mock_session.__aenter__.return_value = mock_session
        mock_session.__aexit__.return_value = None

        mock_task = MagicMock()
        mock_task.url = "https://google.com"
        mock_task.short_link = "abc123"

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_task
        mock_session.execute.return_value = mock_result

        with patch(
            "repositories.task.async_session_factory",
            return_value=mock_session,
        ):
            result = await TaskRepository.get_by_short_link("abc123")

            assert result is not None
            assert result.url == "https://google.com"
            assert result.short_link == "abc123"

    async def test_get_by_short_link_not_found(self):
        mock_session = AsyncMock()
        mock_session.__aenter__.return_value = mock_session
        mock_session.__aexit__.return_value = None

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        with patch(
            "repositories.task.async_session_factory",
            return_value=mock_session,
        ):
            result = await TaskRepository.get_by_short_link("notexist")

            assert result is None


class TestTaskRepositoryGetAll:
    async def test_get_all_empty(self):
        mock_session = AsyncMock()
        mock_session.__aenter__.return_value = mock_session
        mock_session.__aexit__.return_value = None

        mock_result = MagicMock()
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = []
        mock_result.scalars.return_value = mock_scalars
        mock_session.execute.return_value = mock_result

        with patch(
            "repositories.task.async_session_factory",
            return_value=mock_session,
        ):
            result = await TaskRepository.get_all()

            assert result == []

    async def test_get_all_with_tasks(self):
        mock_session = AsyncMock()
        mock_session.__aenter__.return_value = mock_session
        mock_session.__aexit__.return_value = None

        mock_task = MagicMock()
        mock_task.id = 1
        mock_task.url = "https://google.com"
        mock_task.short_link = "abc123"
        mock_task.created_at = datetime.now()
        mock_task.updated_at = datetime.now()
        mock_task.is_active = True
        mock_task.is_deleted = False

        mock_result = MagicMock()
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = [mock_task]
        mock_result.scalars.return_value = mock_scalars
        mock_session.execute.return_value = mock_result

        with patch(
            "repositories.task.async_session_factory",
            return_value=mock_session,
        ):
            result = await TaskRepository.get_all()

            assert len(result) == 1
            assert result[0].url == "https://google.com"
            assert result[0].short_link == "abc123"
