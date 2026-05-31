from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

from services.task import TaskService
from services.url import build_redirect_url

router = APIRouter()
task_service = TaskService()


@router.get("/{short_link}")
async def redirect_to_url(short_link: str) -> RedirectResponse:
    task = await task_service.get_by_short_link(short_link)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return RedirectResponse(
        url=build_redirect_url(task.url),
        status_code=307,
    )
