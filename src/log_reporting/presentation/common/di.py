from dataclasses import dataclass, field
from typing import cast


@dataclass(frozen=True, unsafe_hash=False)
class IoCContainer:
    _dependecy_by_type: dict[object, object] = field(default_factory=dict)

    def get[T](self, type_: type[T], /) -> T:
        return cast(T, self._dependecy_by_type[type_])

    def provide[T](self, value: T, *, provides: type[T] | None) -> None:
        if provides is None:
            provides = type(value)

        self._dependecy_by_type[provides] = value

    def copy(self) -> "IoCContainer":
        return IoCContainer(dict(self._dependecy_by_type))
