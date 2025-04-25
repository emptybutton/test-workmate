from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC
from datetime import datetime as datetime_cls


class NotUTCTimeError(Exception): ...


@dataclass(kw_only=True, frozen=True)
class Time:
    """
    :raises iam.entities.time.time.NotUTCTimeError:
    """

    datetime: datetime_cls

    def __post_init__(self) -> None:
        if self.datetime.tzinfo != UTC:
            raise NotUTCTimeError

    def __gt__(self, time: "Time") -> bool:
        return self.datetime > time.datetime

    def __ge__(self, time: "Time") -> bool:
        return self.datetime >= time.datetime

    def map(self, next: Callable[[datetime_cls], datetime_cls]) -> "Time":
        return Time(datetime=next(self.datetime))
