# -*- coding: utf-8 -*-
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from .models import LogEntry as LogEntryModel
from .schemas import (
    LogEntry as LogEntrySchema, 
    LogEntryBase as LEBaseSchema
)


def process_entry(db_entry: LogEntryModel) -> LogEntrySchema:
    return LogEntrySchema(
        pk=db_entry.pk,
        message=db_entry.message,
        level=db_entry.level,
        timestamp=db_entry.timestamp,
    )


async def get_log_entries(
    session: AsyncSession, skip: int = 0, limit: int = 200
) -> List[LogEntrySchema]:
    result = await session.execute(
        select(LogEntryModel).offset(skip).limit(limit)
    )
    logs = result.scalars().all()
    return [process_entry(log) for log in logs]


async def create_log_entry(
    session: AsyncSession, entry: LEBaseSchema
) -> LogEntrySchema:
    db_entry = LogEntryModel(message=entry.message, level=entry.level)
    session.add(db_entry)
    await session.commit()
    await session.refresh(db_entry)
    return process_entry(db_entry)
