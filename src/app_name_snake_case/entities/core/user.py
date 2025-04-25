from dataclasses import dataclass
from uuid import UUID, uuid4

from effect import IdentifiedValue, New, new


@dataclass(kw_only=True, frozen=True)
class User(IdentifiedValue[UUID]):
    name: str


def registered_user_when(*, user_name: str) -> New[User]:
    return new(User(id=uuid4(), name=user_name))
