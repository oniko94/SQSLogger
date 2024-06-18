# -*- coding: utf-8 -*-
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator

from core.config import DB_URL

engine = create_async_engine(DB_URL)


def get_session() -> async_sessionmaker[AsyncSession]:
    """
    Instantiate and retrieve the async context manager for session initialization.
    We have to do it this way because we can't do it the default FastAPI way with Depends
    Since we use it outside of FastAPI context in a custom worker
    """
    return async_sessionmaker(
        bind=engine, 
        class_=AsyncSession, 
        expire_on_commit=False
    )
