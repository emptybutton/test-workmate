from dataclasses import dataclass
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app_name_snake_case.application.ports.users import Users
from app_name_snake_case.entities.core.user import User
from app_name_snake_case.infrastructure.app_name_snake_case.in_memory_storage import (  # noqa: E501
    TransactionalInMemoryStorage,
)
from app_name_snake_case.infrastructure.sqlalchemy import orm  # noqa: F401


@dataclass(kw_only=True, slots=True)
class InMemoryUsers(Users, TransactionalInMemoryStorage[User]):
    async def user_with_id(self, id: UUID) -> User | None:
        return self.select_one(lambda user: user.id == id)


@dataclass(kw_only=True, frozen=True, slots=True)
class InPostgresUsers(Users):
    session: AsyncSession

    async def user_with_id(self, id: UUID) -> User | None:
        return await self.session.get(User, id)
