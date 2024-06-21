# -*- coding: utf-8 -*-
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .database.models import LogEntry
from .dto import log_entry


# TODO: Implement redis caching
# async def get_log_entries(
#     limit: int = 200,
#     skip: int = 0,
#     session: AsyncSession = Depends(get_session),
# ) -> list[log_entry.ModelDTO]:
#     result = await session.execute(
#         select(LogEntry).offset(skip).limit(limit)
#     )
#     logs = result.scalars().all()
#     return [log_entry.map_dto(log) for log in logs]


async def save_log_entry(
    data: log_entry.BaseDTO,
    session_ctx: async_sessionmaker[AsyncSession],
) -> log_entry.ModelDTO:
    async with session_ctx() as session:
        entry = LogEntry(message=data.message, level=data.level)
        session.add(entry)
        await session.commit()
        return log_entry.map_dto(entry)
