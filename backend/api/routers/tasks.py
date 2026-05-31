from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from schemas import STask, STaskAdd, STaskResponseAdd
from services.task import TaskService
from services.url import InvalidUrlError

router = APIRouter(prefix="/api/v1")
task_service = TaskService()


@router.post("/shorten")
async def shorten_url(
    task_add: Annotated[STaskAdd, Depends()],
) -> STaskResponseAdd:
    try:
        task_short_link = await task_service.shorten(task_add)
    except InvalidUrlError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return STaskResponseAdd(task_short_link=task_short_link)


@router.get("/home")
async def get_home() -> list[STask]:
    return await task_service.get_all()
