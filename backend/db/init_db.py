from db.base import ModelBase
from db.session import engine


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(ModelBase.metadata.create_all)


async def delete_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(ModelBase.metadata.drop_all)
