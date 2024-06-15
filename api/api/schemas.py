# -*- coding: utf-8 -*-
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class LogEntryBase(BaseModel):
    message: str
    level: str


class LogEntry(LogEntryBase):
    model_config = ConfigDict(from_attributes=True)
    pk: int
    timestamp: datetime
