from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.routers.redirect import router as redirect_router
from api.routers.tasks import router as tasks_router
from cache import close_redis, init_redis
from db.init_db import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    await init_redis()
    yield
    await close_redis()


def create_app() -> FastAPI:
    application = FastAPI(lifespan=lifespan)
    application.include_router(tasks_router)
    application.include_router(redirect_router)
    return application


app = create_app()
