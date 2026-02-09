import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from repository import TaskRepository
from schemas import STaskAdd


pytestmark = pytest.mark.anyio


class TestTaskRepositoryAddOne:
    """Тесты для TaskRepository.add_one."""

    async def test_add_one_generates_unique_code(self):
        """Проверка генерации уникального кода."""
        mock_session = AsyncMock()
        mock_session.__aenter__.return_value = mock_session
        mock_session.__aexit__.return_value = None

        # Первый запрос - код существует, второй - нет
        mock_result_exists = MagicMock()
        mock_result_exists.scalar_one_or_none.return_value = MagicMock()  # существует
        
        mock_result_not_exists = MagicMock()
        mock_result_not_exists.scalar_one_or_none.return_value = None  # не существует

        mock_session.execute.side_effect = [mock_result_exists, mock_result_not_exists]
        
        # add и commit - синхронные методы
        mock_session.add = MagicMock()
        mock_session.commit = AsyncMock()

        mock_task = MagicMock()
        mock_task.short_link = "abc123"

        with patch("repository.new_session", return_value=mock_session):
            with patch("repository.TaskOrm") as MockTaskOrm:
                MockTaskOrm.return_value = mock_task
                MockTaskOrm.short_link = "short_link"
                
                with patch("repository.generate_short_code", side_effect=["exists", "abc123"]):
                    with patch("repository.select"):
                        data = STaskAdd(url="https://google.com")
                        result = await TaskRepository.add_one(data)

                        assert result == "abc123"
                        assert mock_session.execute.call_count == 2
                        mock_session.add.assert_called_once()


class TestTaskRepositoryGetByShortLink:
    """Тесты для TaskRepository.get_by_short_link."""

    async def test_get_by_short_link_found(self):
        """Ссылка найдена."""
        mock_session = AsyncMock()
        mock_session.__aenter__.return_value = mock_session
        mock_session.__aexit__.return_value = None

        mock_task = MagicMock()
        mock_task.url = "https://google.com"
        mock_task.short_link = "abc123"

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_task
        mock_session.execute.return_value = mock_result

        with patch("repository.new_session", return_value=mock_session):
            result = await TaskRepository.get_by_short_link("abc123")

            assert result is not None
            assert result.url == "https://google.com"
            assert result.short_link == "abc123"

    async def test_get_by_short_link_not_found(self):
        """Ссылка не найдена."""
        mock_session = AsyncMock()
        mock_session.__aenter__.return_value = mock_session
        mock_session.__aexit__.return_value = None

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        with patch("repository.new_session", return_value=mock_session):
            result = await TaskRepository.get_by_short_link("notexist")

            assert result is None


class TestTaskRepositoryGetAll:
    """Тесты для TaskRepository.get_all."""

    async def test_get_all_empty(self):
        """Пустой список."""
        mock_session = AsyncMock()
        mock_session.__aenter__.return_value = mock_session
        mock_session.__aexit__.return_value = None

        mock_result = MagicMock()
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = []
        mock_result.scalars.return_value = mock_scalars
        mock_session.execute.return_value = mock_result

        with patch("repository.new_session", return_value=mock_session):
            result = await TaskRepository.get_all()

            assert result == []

    async def test_get_all_with_tasks(self):
        """Список с задачами."""
        from datetime import datetime

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

        with patch("repository.new_session", return_value=mock_session):
            result = await TaskRepository.get_all()

            assert len(result) == 1
            assert result[0].url == "https://google.com"
            assert result[0].short_link == "abc123"
