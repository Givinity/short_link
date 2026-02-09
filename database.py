from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase
from typing import Optional
from datetime import datetime



engine = create_async_engine(
    "sqlite+aiosqlite:///./shortlink.db"
)

new_session = async_sessionmaker(
    engine,
    expire_on_commit=False
)


class ModelBase(DeclarativeBase):
    pass

class TaskOrm(ModelBase):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    short_link: Mapped[str]
    url: Mapped[str]
    created_at: Mapped[Optional[datetime]] = mapped_column(default=datetime.now)
    updated_at: Mapped[Optional[datetime]] = mapped_column(default=datetime.now, onupdate=datetime.now)
    is_active: Mapped[bool]
    is_deleted: Mapped[bool]


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(ModelBase.metadata.create_all)

async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(ModelBase.metadata.drop_all)