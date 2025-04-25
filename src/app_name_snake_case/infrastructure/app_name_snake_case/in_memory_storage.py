from collections.abc import Callable, Iterator
from copy import deepcopy
from dataclasses import dataclass, field


class NoTranasctionError(Exception): ...


@dataclass(kw_only=True)
class TransactionalInMemoryStorage[ValueT]:
    _storage: list[ValueT]
    _snapshots: list[list[ValueT]] = field(init=False)

    def __iter__(self) -> Iterator[ValueT]:
        return iter(list(self._storage))

    def __bool__(self) -> bool:
        return bool(self._storage)

    def __len__(self) -> int:
        return len(self._storage)

    def begin(self) -> None:
        self._snapshots.append(deepcopy(self._storage))

    def commit(self) -> None:
        self._validate_has_snapshots()
        self._snapshots.pop()

    def rollback(self) -> None:
        self._validate_has_snapshots()
        snapshot = self._snapshots.pop()
        self._storage = snapshot

    def select_many(
        self, is_selected: Callable[[ValueT], bool]
    ) -> tuple[ValueT, ...]:
        return tuple(value for value in self._storage if is_selected(value))

    def select_one(
        self, is_selected: Callable[[ValueT], bool]
    ) -> ValueT | None:
        for value in self._storage:
            if is_selected(value):
                return value

        return None

    def _validate_has_snapshots(self) -> None:
        if not self._snapshots:
            raise NoTranasctionError
