# -*- coding: utf-8 -*-
import logging
import os
import sys

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator

from .models import Base


logger = logging.getLogger("uvicorn.error")
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL is None:
    logger.error("No database address found in env; Exiting...")
    sys.exit(1)

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
