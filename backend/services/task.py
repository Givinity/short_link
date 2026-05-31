from sqlalchemy.exc import IntegrityError

from cache.redis import get_redis
from cache.task_cache import TaskCache
from db.session import async_session_factory
from repositories.task import TaskRepository
from schemas import STask, STaskAdd, STaskResponseGet
from services.short_link import generate_short_code_from_url
from services.url import validate_url


class TaskService:
    def __init__(
        self,
        repository: type[TaskRepository] = TaskRepository,
        cache: TaskCache | None = None,
    ) -> None:
        self._repository = repository
        self._cache = cache

    def _get_cache(self) -> TaskCache | None:
        if self._cache is not None:
            return self._cache
        try:
            return TaskCache(get_redis())
        except RuntimeError:
            return None

    @staticmethod
    def _to_response(task_url: str, short_link: str) -> STaskResponseGet:
        return STaskResponseGet(url=task_url, short_link=short_link)

    async def _cache_task(self, url: str, short_link: str) -> None:
        cache = self._get_cache()
        if cache is None:
            return
        await cache.set_by_short_link(self._to_response(url, short_link))

    async def shorten(self, data: STaskAdd) -> str:
        data.url = validate_url(data.url)
        async with async_session_factory() as session:
            existing = await self._repository.find_by_url(session, data.url)
            if existing:
                await self._cache_task(existing.url, existing.short_link)
                return existing.short_link

            attempt = 0
            while True:
                short_code = generate_short_code_from_url(data.url, attempt=attempt)
                task = self._repository.build_task(data, short_code)
                session.add(task)
                try:
                    await session.commit()
                    await self._cache_task(task.url, task.short_link)
                    return task.short_link
                except IntegrityError:
                    await session.rollback()
                    existing = await self._repository.find_by_url(session, data.url)
                    if existing:
                        await self._cache_task(existing.url, existing.short_link)
                        return existing.short_link
                    attempt += 1

    async def get_all(self) -> list[STask]:
        return await self._repository.get_all()

    async def get_by_short_link(self, short_link: str) -> STaskResponseGet | None:
        cache = self._get_cache()
        if cache is not None:
            cached = await cache.get_by_short_link(short_link)
            if cached is not None:
                return cached

        task = await self._repository.get_by_short_link(short_link)
        if task is not None and cache is not None:
            await cache.set_by_short_link(task)
        return task
