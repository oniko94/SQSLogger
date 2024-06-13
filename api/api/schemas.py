# -*- coding: utf-8 -*-
from typing import datetime
from pydantic import BaseModel


class LogEntryBase(BaseModel):
    message: str
    level: str


class LogEntry(LogEntryBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
