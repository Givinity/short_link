from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from sqlalchemy.exc import IntegrityError

from schemas import STaskAdd, STaskResponseGet
from services.task import TaskService

pytestmark = pytest.mark.anyio


class TestTaskServiceShorten:
    async def test_shorten_retries_on_short_link_collision(self):
        mock_session = AsyncMock()
        mock_session.__aenter__.return_value = mock_session
        mock_session.__aexit__.return_value = None
        mock_session.add = MagicMock()
        mock_session.rollback = AsyncMock()
        mock_session.commit = AsyncMock(
            side_effect=[IntegrityError("stmt", {}, Exception("dup")), None]
        )

        mock_task = MagicMock()
        mock_task.short_link = "abc123"

        with patch("services.task.async_session_factory", return_value=mock_session):
            with patch(
                "services.task.TaskRepository.find_by_url",
                new_callable=AsyncMock,
                return_value=None,
            ):
                with patch(
                    "services.task.TaskRepository.build_task",
                    return_value=mock_task,
                ):
                    with patch(
                        "services.task.generate_short_code_from_url",
                        side_effect=["collision", "abc123"],
                    ):
                        result = await TaskService().shorten(
                            STaskAdd(url="https://google.com")
                        )

                        assert result == "abc123"
                        assert mock_session.commit.call_count == 2
                        assert mock_session.rollback.call_count == 1

    async def test_shorten_returns_existing_after_url_race_on_commit(self):
        mock_session = AsyncMock()
        mock_session.__aenter__.return_value = mock_session
        mock_session.__aexit__.return_value = None
        mock_session.add = MagicMock()
        mock_session.rollback = AsyncMock()
        mock_session.commit = AsyncMock(
            side_effect=IntegrityError("stmt", {}, Exception("dup"))
        )

        mock_existing = MagicMock()
        mock_existing.short_link = "race123"

        with patch("services.task.async_session_factory", return_value=mock_session):
            with patch(
                "services.task.TaskRepository.find_by_url",
                new_callable=AsyncMock,
                side_effect=[None, mock_existing],
            ):
                with patch(
                    "services.task.generate_short_code_from_url",
                    return_value="newcode",
                ):
                    result = await TaskService().shorten(
                        STaskAdd(url="https://google.com")
                    )

                    assert result == "race123"
                    mock_session.rollback.assert_called_once()

    async def test_shorten_returns_existing_for_same_url(self):
        mock_existing = MagicMock()
        mock_existing.short_link = "existing1"

        mock_session = AsyncMock()
        mock_session.__aenter__.return_value = mock_session
        mock_session.__aexit__.return_value = None

        with patch("services.task.async_session_factory", return_value=mock_session):
            with patch(
                "services.task.TaskRepository.find_by_url",
                new_callable=AsyncMock,
                return_value=mock_existing,
            ):
                with patch(
                    "services.task.generate_short_code_from_url"
                ) as mock_generate:
                    result = await TaskService().shorten(
                        STaskAdd(url="https://google.com")
                    )

                    assert result == "existing1"
                    mock_generate.assert_not_called()
                    mock_session.add.assert_not_called()


class TestTaskServiceGetByShortLink:
    async def test_returns_cached_task_without_db(self):
        cached = STaskResponseGet(url="https://google.com", short_link="abc123")
        mock_cache = AsyncMock()
        mock_cache.get_by_short_link = AsyncMock(return_value=cached)

        with patch(
            "services.task.TaskRepository.get_by_short_link",
            new_callable=AsyncMock,
        ) as mock_get:
            result = await TaskService(cache=mock_cache).get_by_short_link("abc123")

            assert result == cached
            mock_get.assert_not_called()

    async def test_loads_from_db_and_caches_on_miss(self):
        db_task = STaskResponseGet(url="https://google.com", short_link="abc123")
        mock_cache = AsyncMock()
        mock_cache.get_by_short_link = AsyncMock(return_value=None)
        mock_cache.set_by_short_link = AsyncMock()

        with patch(
            "services.task.TaskRepository.get_by_short_link",
            new_callable=AsyncMock,
            return_value=db_task,
        ):
            result = await TaskService(cache=mock_cache).get_by_short_link("abc123")

            assert result == db_task
            mock_cache.set_by_short_link.assert_awaited_once_with(db_task)
