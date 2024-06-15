# -*- coding: utf-8 -*-
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from . import db, models, schemas
from .crud import create_log_entry


app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await db.initialize()


@app.post("/log_entry", response_model=schemas.LogEntry)
async def write_entry(
    entry: schemas.LogEntry, session: AsyncSession = Depends(db.get_session)
):
    log_entry = await create_log_entry(session, entry)
    return log_entry
