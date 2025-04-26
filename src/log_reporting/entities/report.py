from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Self

from log_reporting.entities.endpoint import Endpoint
from log_reporting.entities.log_level_counter import LogLevelCounter


class Report(ABC):
    @abstractmethod
    def expand_with(self, other: Self, /) -> None: ...

    @classmethod
    @abstractmethod
    def empty_report(cls) -> Self: ...


@dataclass
class HandlerReport(Report):
    endpoint_map: dict[Endpoint, LogLevelCounter]

    def expand_with(self, other: Self) -> None:
        for endpoint, other_log_level_counter in other.endpoint_map.items():
            self_log_level_counter = self.endpoint_map.get(endpoint)

            if self_log_level_counter is None:
                self.endpoint_map[endpoint] = other_log_level_counter.copy()
                continue

            self_log_level_counter.expand_with(other_log_level_counter)

    @property
    def total_requests(self) -> int:
        return sum(
            sum(log_level_counter.map.values())
            for log_level_counter in self.endpoint_map.values()
        )

    @classmethod
    def empty_report(cls) -> "HandlerReport":
        return HandlerReport(endpoint_map=dict())
