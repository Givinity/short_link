from sqlalchemy import select

from database import TaskOrm, new_session
from schemas import STask, STaskAdd, STaskResponseGet
from services import generate_short_code


class TaskRepository:
    @classmethod
    async def add_one(cls, data: STaskAdd):
        async with new_session() as session:
            # Генерируем уникальный short_link
            while True:
                short_code = generate_short_code()
                existing = await session.execute(
                    select(TaskOrm).where(TaskOrm.short_link == short_code)
                )
                if not existing.scalar_one_or_none():
                    break

            task = TaskOrm(
                url=data.url,
                short_link=short_code,
                is_active=data.is_active,
                is_deleted=data.is_deleted,
            )
            session.add(task)
            await session.commit()
            return task.short_link

    @classmethod
    async def get_all(cls) -> list[STask]:
        async with new_session() as session:
            query = select(TaskOrm)
            result = await session.execute(query)
            task_models = result.scalars().all()
            tasks = [
                STask(
                    id=task.id,
                    url=task.url,
                    short_link=task.short_link,
                    created_at=task.created_at,
                    updated_at=task.updated_at,
                    is_active=task.is_active,
                    is_deleted=task.is_deleted,
                )
                for task in task_models
            ]
            return tasks

    @classmethod
    async def get_by_short_link(cls, short_link: str):
        async with new_session() as session:
            query = select(TaskOrm).where(
                TaskOrm.short_link == short_link,
            )
            result = await session.execute(query)
            task_model = result.scalar_one_or_none()
            if not task_model:
                return None
            return STaskResponseGet(
                url=task_model.url, short_link=task_model.short_link
            )
