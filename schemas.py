from datetime import datetime

from pydantic import BaseModel


class STaskAdd(BaseModel):
    url: str
    created_at: datetime | None = datetime.now()
    updated_at: datetime | None = datetime.now()
    is_active: bool = True
    is_deleted: bool = False


class STask(STaskAdd):
    id: int
    url: str
    short_link: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
    is_deleted: bool


class STaskResponseAdd(BaseModel):
    ok: bool = True
    task_short_link: str


class STaskResponseGet(BaseModel):
    url: str
    short_link: str
