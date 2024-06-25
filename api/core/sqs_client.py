# -*- coding: utf-8 -*-
import asyncio
import aioboto3

from typing import AsyncGenerator

from .config import AWS_ENDPOINT


class AsyncSQSClient:
    """
    A simple factory reading credentials from the environment variables
    Returns an asynchronous context manager
    """
    def __init__(self, **kwargs):
        pass

    def create_client(self) -> AsyncGenerator:
        session = aioboto3.Session()

        if AWS_ENDPOINT is None:
            return session.client("sqs")
        else:
            return session.client("sqs", endpoint_url=AWS_ENDPOINT)
