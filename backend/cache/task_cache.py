import logging

from redis.asyncio import Redis
from redis.exceptions import RedisError

from config import CACHE_TTL_SECONDS
from schemas import STaskResponseGet

logger = logging.getLogger(__name__)

TASK_KEY_PREFIX = "shortlink:task:"


class TaskCache:
    def __init__(
        self,
        redis: Redis,
        ttl_seconds: int = CACHE_TTL_SECONDS,
    ) -> None:
        self._redis = redis
        self._ttl_seconds = ttl_seconds

    @staticmethod
    def _key(short_link: str) -> str:
        return f"{TASK_KEY_PREFIX}{short_link}"

    async def get_by_short_link(self, short_link: str) -> STaskResponseGet | None:
        try:
            data = await self._redis.get(self._key(short_link))
        except RedisError:
            logger.exception("Redis get failed for short_link=%s", short_link)
            return None

        if data is None:
            return None

        try:
            await self._redis.expire(self._key(short_link), self._ttl_seconds)
        except RedisError:
            logger.exception("Redis expire failed for short_link=%s", short_link)

        return STaskResponseGet.model_validate_json(data)

    async def set_by_short_link(self, task: STaskResponseGet) -> None:
        try:
            await self._redis.set(
                self._key(task.short_link),
                task.model_dump_json(),
                ex=self._ttl_seconds,
            )
        except RedisError:
            logger.exception("Redis set failed for short_link=%s", task.short_link)
