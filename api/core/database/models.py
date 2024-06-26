# -*- coding: utf-8 -*-
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    pass


class LogEntry(Base):
    """
    SQL Schema:
    pk SERIAL PRIMARY KEY
    message TEXT NOT NULL
    level TEXT NOT NULL
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    """

    __tablename__ = "log_entries"
    pk = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    message = sa.Column(sa.Text, nullable=False)
    level = sa.Column(sa.Text, nullable=False)
    timestamp = sa.Column(
        sa.DateTime,
        server_default=sa.func.current_timestamp(),
        nullable=False,
    )
