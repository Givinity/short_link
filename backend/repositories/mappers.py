from db.models import TaskOrm
from schemas import STask, STaskResponseGet


def to_task_schema(task: TaskOrm) -> STask:
    return STask(
        id=task.id,
        url=task.url,
        short_link=task.short_link,
        created_at=task.created_at,
        updated_at=task.updated_at,
        is_active=task.is_active,
        is_deleted=task.is_deleted,
    )


def to_task_response_get(task: TaskOrm) -> STaskResponseGet:
    return STaskResponseGet(url=task.url, short_link=task.short_link)
