from collections.abc import AsyncIterator, Sequence
from contextlib import asynccontextmanager
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app_name_snake_case.infrastructure.app_name_snake_case.in_memory_storage import (  # noqa: E501
    TransactionalInMemoryStorage,
)


@asynccontextmanager
async def in_postgres_transaction_when(
    *, session: AsyncSession
) -> AsyncIterator[None]:
    async with session.begin():
        yield


@asynccontextmanager
async def in_memory_transaction_for(
    storages: Sequence[TransactionalInMemoryStorage[Any]]
) -> AsyncIterator[None]:
    for storage in storages:
        storage.begin()

    try:
        yield
    except Exception as error:
        for storage in storages:
            storage.rollback()
        raise error from error
    else:
        for storage in storages:
            storage.commit()
