import asyncpg
from typing import AsyncGenerator
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from server.settings import settings

engine = create_async_engine(url=settings.DATABASE_URL, echo=True)

async_session_maker = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Generator func for creating db sessions."""
    async with async_session_maker() as session:
        yield session

async def create_db_if_not_exists(db_url: str) -> None:
    db_name = db_url.split('/')[-1]
    server_url = (
        "/".join(db_url.split("/")[:-1])
    ).replace("postgresql+asyncpg://", "postgresql://")

    async with asyncpg.create_pool(server_url) as pool:
        async with pool.acquire() as conn:
            result = await conn.fetch(
                "SELECT 1 FROM pg_database WHERE datname = $1", db_name
            )
            if not result:
                await conn.execute(f"CREATE DATABASE {db_name}")


async def init_db() -> None:
    await create_db_if_not_exists(settings.DATABASE_URL)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
