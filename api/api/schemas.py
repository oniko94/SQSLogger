# -*- coding: utf-8 -*-
from datetime import datetime
from pydantic import BaseModel


class LogEntryBase(BaseModel):
    message: str
    level: str


class LogEntry(LogEntryBase):
    pk: int
    timestamp: datetime

    class Config:
        from_attributes = True
