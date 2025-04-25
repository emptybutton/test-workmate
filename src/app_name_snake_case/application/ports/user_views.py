from abc import ABC, abstractmethod
from uuid import UUID

from app_name_snake_case.entities.core.user import User


class UserViews[UserViewT, UserWithIDViewT](ABC):
    @abstractmethod
    async def view_of_user(self, user: User, /) -> UserViewT: ...

    @abstractmethod
    async def view_of_user_with_id(
        self, user_id: UUID | None, /
    ) -> UserWithIDViewT:
        ...
