from sqlalchemy.orm import registry

from app_name_snake_case.entities.core.user import User
from app_name_snake_case.infrastructure.sqlalchemy.tables import (
    metadata,
    user_table,
)


def _mutable[T: type](type_: T) -> T:
    type_.__setattr__ = object.__setattr__  # type: ignore[method-assign, assignment]
    type_.__delattr__ = object.__delattr__  # type: ignore[method-assign, assignment]

    return type_


mapper_registry = registry(metadata=metadata)

mapper_registry.map_imperatively(_mutable(User), user_table)

# Alias.__composite_values__ = lambda self: (self.text,)  # type: ignore[attr-defined]  # noqa: E501, ERA001
