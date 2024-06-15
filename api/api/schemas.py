# -*- coding: utf-8 -*-
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class LogEntry(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    message: str
    level: str
