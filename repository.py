from database import new_session
from schemas import STaskAdd
from database import TaskOrm
from sqlalchemy import select
from schemas import STask


class TaskRepository:
    @classmethod
    async def add_one(cls, data: STaskAdd):
        async with new_session() as session:
            task_dict = data.model_dump()
            
            task = TaskOrm(**task_dict)
            session.add(task)
            await session.flush()
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