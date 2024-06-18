# -*- coding: utf-8 -*-
import asyncio
import aioboto3

from typing import AsyncGenerator

from .config import (
    AWS_ACCESS_KEY_ID,
    AWS_ENDPOINT,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION,
)


class AsyncSQSClient:
    """
    A simple factory reading credentials from the environment variables
    Returns an asynchronous context manager
    """

    def __init__(self, **kwargs):
        self.access_key = AWS_ACCESS_KEY_ID
        self.secret_key = AWS_SECRET_ACCESS_KEY
        self.region = AWS_REGION

    def create_client(self) -> AsyncGenerator:
        session = aioboto3.Session(
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region,
        )

        if AWS_ENDPOINT is None:
            return session.client("sqs")
        else:
            return session.client("sqs", endpoint_url=AWS_ENDPOINT)
