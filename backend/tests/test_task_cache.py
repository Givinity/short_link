from unittest.mock import AsyncMock

import pytest
from redis.exceptions import ConnectionError as RedisConnectionError

from cache.task_cache import TASK_KEY_PREFIX, TaskCache
from schemas import STaskResponseGet

pytestmark = pytest.mark.anyio


@pytest.fixture
def redis_mock():
    mock = AsyncMock()
    mock.get = AsyncMock(return_value=None)
    mock.set = AsyncMock()
    mock.expire = AsyncMock()
    return mock


@pytest.fixture
def task_cache(redis_mock):
    return TaskCache(redis_mock, ttl_seconds=86400)


class TestTaskCache:
    async def test_get_returns_none_on_miss(self, task_cache, redis_mock):
        redis_mock.get.return_value = None

        result = await task_cache.get_by_short_link("abc123")

        assert result is None
        redis_mock.expire.assert_not_called()

    async def test_get_returns_task_and_refreshes_ttl(self, task_cache, redis_mock):
        task = STaskResponseGet(url="https://google.com", short_link="abc123")
        redis_mock.get.return_value = task.model_dump_json()

        result = await task_cache.get_by_short_link("abc123")

        assert result == task
        redis_mock.expire.assert_awaited_once_with(
            f"{TASK_KEY_PREFIX}abc123",
            86400,
        )

    async def test_set_stores_task_with_ttl(self, task_cache, redis_mock):
        task = STaskResponseGet(url="https://google.com", short_link="abc123")

        await task_cache.set_by_short_link(task)

        redis_mock.set.assert_awaited_once_with(
            f"{TASK_KEY_PREFIX}abc123",
            task.model_dump_json(),
            ex=86400,
        )

    async def test_get_returns_none_when_redis_fails(self, task_cache, redis_mock):
        redis_mock.get.side_effect = RedisConnectionError("redis down")

        result = await task_cache.get_by_short_link("abc123")

        assert result is None
