from fastapi import APIRouter
from typing import Annotated
from fastapi import Depends
from schemas import STaskAdd
from repository import TaskRepository
from schemas import STaskResponseAdd
from fastapi import HTTPException
from fastapi.responses import RedirectResponse


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


redirect_router = APIRouter()

@redirect_router.get("/{short_link}")
async def redirect_to_url(short_link: str):
    task = await TaskRepository.get_by_short_link(short_link)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if "http" not in task.url:
        task.url = f"https://{task.url}"
    return RedirectResponse(url=task.url, status_code=307)