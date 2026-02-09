from re import S
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ShortLink(BaseModel):
    short_link: str

class STaskAdd(BaseModel):
    url: str
    short_link: str
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()
    is_active: bool
    is_deleted: bool

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
