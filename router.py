from fastapi import APIRouter
from typing import Annotated
from fastapi import Depends
from schemas import STaskAdd
from repository import TaskRepository
from schemas import STaskResponseAdd


router = APIRouter(
    prefix="/api/v1",
)

@router.post("/shorten")
async def shorten_url(
        task_add: Annotated[STaskAdd, Depends(STaskAdd)]
    ) -> STaskResponseAdd:
    task_short_link = await TaskRepository.add_one(task_add)
    return {
        "ok": True,
        "task_short_link": task_short_link
    }
@router.get("/home")
async def get_home():
    tasks = await TaskRepository.get_all()
    return tasks
