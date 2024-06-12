# -*- coding: utf-8 -*-
from fastapi import FastAPI
from .schemas import LogEntry


app = FastAPI()


@app.post("/log_entry")
async def log_entry(entry: LogEntry):
    print(entry)
    return entry
