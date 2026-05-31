from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import TaskOrm
from db.session import async_session_factory
from repositories.mappers import to_task_response_get, to_task_schema
from schemas import STask, STaskAdd, STaskResponseGet


class TaskRepository:
    @staticmethod
    async def find_by_url(session: AsyncSession, url: str) -> TaskOrm | None:
        result = await session.execute(select(TaskOrm).where(TaskOrm.url == url))
        return result.scalar_one_or_none()

    @staticmethod
    async def find_by_short_link(
        session: AsyncSession,
        short_link: str,
    ) -> TaskOrm | None:
        result = await session.execute(
            select(TaskOrm).where(TaskOrm.short_link == short_link)
        )
        return result.scalar_one_or_none()

    @staticmethod
    def build_task(data: STaskAdd, short_link: str) -> TaskOrm:
        return TaskOrm(
            url=data.url,
            short_link=short_link,
            is_active=data.is_active,
            is_deleted=data.is_deleted,
        )

    @classmethod
    async def get_all(cls) -> list[STask]:
        async with async_session_factory() as session:
            result = await session.execute(select(TaskOrm))
            return [to_task_schema(task) for task in result.scalars().all()]

    @classmethod
    async def get_by_short_link(cls, short_link: str) -> STaskResponseGet | None:
        async with async_session_factory() as session:
            task = await cls.find_by_short_link(session, short_link)
            if not task:
                return None
            return to_task_response_get(task)
