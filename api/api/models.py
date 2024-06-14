# -*- coding: utf-8 -*-
import os
import sys
import sqlalchemy as sa

from datetime import datetime
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase


try:
    DATABASE_URL = os.environ["DATABASE_URL"]
except KeyError:
    print("No database address found in env; Exiting...", file=sys.stderr)
    sys.exit(1)
else:
    engine = create_async_engine(DATABASE_URL)
    AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class LogEntry(Base):
    __tablename__ = "log_entries"
    pk = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    message = sa.Column(sa.Text, nullable=False)
    level = sa.Column(sa.Text, nullable=False)
    timestamp = sa.Column(
        sa.DateTime, server_default=sa.func.current_timestamp(), nullable=False
    )
