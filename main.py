from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import create_tables, delete_tables
from router import redirect_router as redirect_router
from router import router as task_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    await create_tables()
    print("Tables created")
    yield
    print("Lifespan ended")


app = FastAPI(lifespan=lifespan)
app.include_router(task_router)
app.include_router(redirect_router)
