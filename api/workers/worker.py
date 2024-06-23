# -*- coding: utf-8 -*-
import asyncio

from core.config import SQS_QUEUE_NAME
from core.database.session import get_session
from core.dto import log_entry
from core.logging import create_logger
from core.services import save_log_entry
from core.sqs_client import AsyncSQSClient


logger = create_logger("api.workers")


class Worker:
    """
        A custom worker class.
        Uses asyncio, but also is expected to run multiprocessed
    """
    def __init__(self) -> None:
        self.queue_url: str = ""

    def start(self) -> None:
        logger.info("Starting a worker process")
        # Instantiate the session client context manager
        # According to boto3 documentation they are not really thread safe
        # So it is better to keep a client instance per process
        # In case of multiprocessing/running in parallel
        sqs_ctx = AsyncSQSClient().create_client()
        session = get_session()

        try:
            asyncio.run(self.__main(sqs_ctx, session))
        except asyncio.CancelledError:
            logger.info("Interrupt signal received. Shutting down...")

    async def __main(self, sqs_ctx, db_session) -> None:
        async with sqs_ctx as sqs:
            queue = await sqs.get_queue_url(QueueName=SQS_QUEUE_NAME)
            self.queue_url = queue["QueueUrl"]

            logger.info(f"Subscribing to {SQS_QUEUE_NAME}.")
            while True:
                # Polling the queue for new messages each 10 seconds
                await self.__handle_messages(sqs, db_session)

    async def __handle_messages(self, sqs_client, db_session) -> None:
        response = await sqs_client.receive_message(
            QueueUrl=self.queue_url,
            WaitTimeSeconds=10, 
            VisibilityTimeout=10
        )

        for message in response.get("Messages", []):
            logger.info(f"Message received!")
            msg_id = message["ReceiptHandle"]
            # Deserialize the message body into a valid log entry object
            entry = log_entry.BaseDTO.parse_raw(message["Body"])
            try:
                logger.info(
                     msg=f"Saving message info to the database..."
                )
                # Save it to the database
                record = await save_log_entry(entry, db_session)
            except Exception:
                logger.exception("Worker process failed;")
            else:
                # Delete the message after
                logger.info(
                    msg=f"Log entry {record.pk} stored to the database;"
                )
                logger.info(
                    msg=f"Deleting message {msg_id} from queue {self.queue_url}"
                )
                await sqs_client.delete_message(
                    QueueUrl=self.queue_url,
                    ReceiptHandle=msg_id
                )
