# -*- coding: utf-8 -*-
import aioboto3
import json
import logging

from base64 import b64decode
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .config import DB_URL, SQS_QUEUE_NAME
from .models import LogEntry as LogEntryModel
from .schemas import (
    LogEntry as LogEntrySchema, 
    LogEntryBase as LEBaseSchema
)
from .sqs import AsyncSQSClient


logger = logging.getLogger(__name__)
# Explicit mapping is more Pythonic
# Also grants more control over data
def process_entry(db_entry: LogEntryModel) -> LogEntrySchema:
    """
    A function used to map the SQLAlchemy ORM fields to Pydantic model ones.

    Parameter
    ---------
    db_entry : api.api.models.LogEntry
        A SQLAlchemy model representation we store in the DB

    Returns
    -------
    api.api.schemas.LogEntry
        A Pydantic representation of the LogEntry data from the DB
    """
    return LogEntrySchema(
        pk=db_entry.pk,
        message=db_entry.message,
        level=db_entry.level,
        timestamp=db_entry.timestamp,
    )


async def get_log_entries(
    session: AsyncSession, skip: int = 0, limit: int = 200
) -> list[LogEntrySchema]:
    result = await session.execute(
        select(LogEntryModel).offset(skip).limit(limit)
    )
    logs = result.scalars().all()
    return [process_entry(log) for log in logs]


async def create_log_entry(
    session: AsyncSession, entry: LEBaseSchema
):
    sqs_ctx = AsyncSQSClient(logger).create_client()

    async with sqs_ctx as sqs:
        logger.info("Retrieving the SQS Queue URL")
        queue = await sqs.get_queue_url(QueueName=SQS_QUEUE_NAME)

        logger.info("Sending the message....")
        await sqs.send_message(
            QueueUrl=queue.get("QueueUrl"),
            MessageBody=entry.model_dump_json(indent=4)
        )
        logger.info("Message sent!")
    return entry
