from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import TYPE_CHECKING, Annotated, Any

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import settings

if TYPE_CHECKING:
    from sqlalchemy import URL


class DatabaseManager:
    def __init__(self, url: str | URL, **kwargs: Any):
        self.engine = create_async_engine(url=url, **kwargs)
        self.session_maker = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            autoflush=False,
        )

    async def session_getter(self) -> AsyncGenerator[AsyncSession]:
        async with self.session_maker() as session:
            yield session


db_manager = DatabaseManager(
    url=settings.db.url,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
    echo=settings.db.echo,
)

SessionDep = Annotated[AsyncSession, Depends(db_manager.session_getter)]
