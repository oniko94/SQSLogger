# -*- coding: utf-8 -*-
from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from .crud import get_log_entries, create_log_entry
from .db import get_session
from .schemas import LogEntry, LogEntryBase


app = FastAPI()


@app.get("/logs", response_model=list[LogEntry])
async def read_logs(
    session: AsyncSession = Depends(get_session),
) -> list[LogEntry]:
    logs = await get_log_entries(session)
    return logs


@app.post("/logs", response_model=LogEntryBase)
async def write_entry(
    entry: LogEntryBase, session: AsyncSession = Depends(get_session)
) -> LogEntry:
    log_entry = await create_log_entry(session, entry)
    return log_entry
