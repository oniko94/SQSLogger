# -*- coding: utf-8 -*-
import asyncio
from concurrent.futures import ProcessPoolExecutor

from core.config import MAX_WORKERS
from .worker import Worker


async def spawn():
    executor = ProcessPoolExecutor(max_workers=MAX_WORKERS)
    loop = asyncio.get_event_loop()
    worker = Worker()

    await loop.run_in_executor(executor, worker.start)


if __name__ == "__main__":
    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    event_loop.run_until_complete(spawn())
