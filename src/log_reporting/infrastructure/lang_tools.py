from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import Any, cast


@dataclass(frozen=True)
class UnpackingCall[R]:
    func: Callable[..., R]

    def __call__(self, args: Iterable[Any]) -> R:
        return self.func(*args)


def slices(range_: range) -> list["slice[int, int, None]"]:
    slices_ = list["slice[int, int, None]"]()

    if range_.step == 1:
        return [cast("slice[int, int, None]", slice(range_.start, range_.stop))]

    range_iter = iter(range_)
    prevous_offset = next(range_iter)

    for offset in range_iter:
        slices_.append(
            cast("slice[int, int, None]", slice(prevous_offset, offset))
        )
        prevous_offset = offset

    slices_.append(
        cast("slice[int, int, None]", slice(prevous_offset, range_.stop))
    )

    return slices_
