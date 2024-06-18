# -*- coding: utf-8 -*-
import asyncio
from .worker import Worker


if __name__ == "__main__":
    worker = Worker()
    asyncio.run(worker.start())
