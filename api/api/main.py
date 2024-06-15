# -*- coding: utf-8 -*-
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from . import db, models, schemas
from .crud import get_log_entries, create_log_entry


app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await db.initialize()


@app.get("/logs", response_model=list[schemas.LogEntry])
async def read_logs(session: AsyncSession = Depends(db.get_session)):
    logs = await get_log_entries(session)
    return logs


@app.post("/log_entry", response_model=schemas.LogEntry)
async def write_entry(
    entry: schemas.LogEntryBase, session: AsyncSession = Depends(db.get_session)
):
    log_entry = await create_log_entry(session, entry)
    return log_entry
