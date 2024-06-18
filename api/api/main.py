# -*- coding: utf-8 -*-
from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import SQS_QUEUE_NAME
from core.database.session import get_session
from core.dto import log_entry
from core.logging import create_logger
from core.sqs_client import AsyncSQSClient


app = FastAPI()

create_logger("uvicorn.error")
create_logger("uvicorn.access")
logger = create_logger("api.endpoints")


@app.get("/healthcheck")
def get_healthcheck() -> None:
    return "OK"


# TODO: implement redis caching
# @app.get("/logs", response_model=list[LogEntryDTO])
# async def read_logs(
#     session: AsyncSession = Depends(get_session),
# ) -> list[LogEntryDTO]:
#     logs = await get_log_entries(session)
#     return logs


@app.post("/logs")
async def send_log_entry(entry: log_entry.BaseDTO) -> None:
    """Offload the log message processing through AWS SQS"""
    # Instantiate the session context
    sqs_ctx = AsyncSQSClient().create_client()

    async with sqs_ctx as sqs:
        logger.info("Retrieving the SQS Queue URL")
        # Retrieve the queue url from the environment variables
        queue = await sqs.get_queue_url(QueueName=SQS_QUEUE_NAME)

        logger.info("Sending the message....")
        await sqs.send_message(
            QueueUrl=queue.get("QueueUrl"),
            MessageBody=entry.model_dump_json(indent=4),
        )
        logger.info("Message sent!")
