# -*- coding: utf-8 -*-
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


async def create_log_entry(
    session: AsyncSession, entry: schemas.LogEntry
) -> models.LogEntry:
    db_entry = models.LogEntry(message=entry.message, level=entry.level)
    session.add(db_entry)
    await session.commit()
    await session.refresh(db_entry)
    return db_entry
