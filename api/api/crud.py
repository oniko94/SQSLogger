# -*- coding: utf-8 -*-
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


def process_entry(db_entry: models.LogEntry) -> schemas.LogEntry:
    return schemas.LogEntry(
        pk=db_entry.pk,
        message=db_entry.message,
        level=db_entry.level,
        timestamp=db_entry.timestamp,
    )


async def get_log_entries(session: AsyncSession, skip: int = 0, limit: int = 200):
    result = await session.execute(select(models.LogEntry).offset(skip).limit(limit))
    logs = result.scalars().all()
    return [process_entry(log) for log in logs]


async def create_log_entry(
    session: AsyncSession, entry: schemas.LogEntryBase
) -> models.LogEntry:
    db_entry = models.LogEntry(message=entry.message, level=entry.level)
    session.add(db_entry)
    await session.commit()
    await session.refresh(db_entry)
    return db_entry
