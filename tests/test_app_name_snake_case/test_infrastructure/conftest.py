from collections.abc import AsyncIterable

from pytest import fixture
from sqlalchemy import NullPool, delete
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)

from app_name_snake_case.infrastructure.sqlalchemy.tables import metadata
from app_name_snake_case.infrastructure.typenv.envs import Envs


@fixture(scope="session")
def engine(envs: Envs) -> AsyncEngine:
    return create_async_engine(envs.postgres_url, poolclass=NullPool)


@fixture(scope="session")
async def _session_session(
    engine: AsyncEngine,
) -> AsyncIterable[AsyncSession]:
    session = AsyncSession(
        engine,
        autoflush=False,
        expire_on_commit=False,
        autobegin=False,
    )

    async with session:
        yield session


@fixture()
async def session(
    _session_session: AsyncSession,
) -> AsyncSession:
    await _clear_db(_session_session)
    return _session_session


async def _clear_db(session: AsyncSession) -> None:
    for table in reversed(metadata.sorted_tables):
        await session.execute(delete(table))
