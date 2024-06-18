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
    # TODO: test if can be used with multiprocessing Pool
    """

    def __init__(self) -> None:
        pass

    async def start(self) -> None:
        logger.info("Worker running")
        # Instantiate the session client context manager
        # According to boto3 documentation they are not really thread safe
        # So it is better to keep a client instance per process
        # In case of multiprocessing/running in parallel
        sqs_ctx = AsyncSQSClient().create_client()
        session = get_session()

        try:
            async with sqs_ctx as sqs:
                logger.info("Retrieving the SQS Queue URL")
                queue = await sqs.get_queue_url(QueueName=SQS_QUEUE_NAME)
                q_url = queue["QueueUrl"]

                logger.info("Awaiting messages...")
                while True:
                    # Polling the queue for new messages each 10 seconds
                    response = await sqs.receive_message(
                        QueueUrl=q_url, 
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
                            log = await save_log_entry(entry, session)
                        except Exception:
                            logger.exception("Worker process failed;")
                        else:
                            # Once the message is saved it is better to delete it to keep the queue clean
                            logger.info(
                                msg=f"Log entry {log.pk} stored to the database;"
                            )
                            logger.info(
                                msg=f"Deleting message {msg_id} from queue {q_url}"
                            )
                            await sqs.delete_message(
                                QueueUrl=q_url, ReceiptHandle=msg_id
                            )
        except asyncio.CancelledError:
            logger.info("Interrupt signal received. Shutting down...")
