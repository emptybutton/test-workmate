from dataclasses import dataclass

from log_reporting.entities.log_level import LogLevel


class NegativeLogLevelCountError(Exception):
    def __init__(self, log_level: LogLevel) -> None:
        super().__init__(log_level)
        self.log_level = log_level


@dataclass
class LogLevelCounter:
    map: dict[LogLevel, int]

    def __post_init__(self) -> None:
        """
        :raises  log_reporting.entities.log_level_counter.NegativeLogLevelCountError:
        """  # noqa: E501

        for log_level in LogLevel:
            if log_level not in self.map:
                self.map[log_level] = 0

            elif self.map[log_level] < 0:
                raise NegativeLogLevelCountError(log_level)

    def copy(self) -> "LogLevelCounter":
        return LogLevelCounter(dict(self.map))

    def expand_with(self, other: "LogLevelCounter") -> None:
        for log_level, count in other.map.items():
            self.map[log_level] += count
