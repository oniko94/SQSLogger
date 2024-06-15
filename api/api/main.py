# -*- coding: utf-8 -*-
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from .crud import get_log_entries, create_log_entry
from .db import get_session, init_db
from .schemas import LogEntry, LogEntryBase


app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/logs", response_model=List[LogEntry])
async def read_logs(
    session: AsyncSession = Depends(get_session),
) -> List[LogEntry]:
    logs = await get_log_entries(session)
    return logs


@app.post("/log_entry", response_model=LogEntry)
async def write_entry(
    entry: LogEntryBase, session: AsyncSession = Depends(get_session)
) -> LogEntry:
    log_entry = await create_log_entry(session, entry)
    return log_entry
