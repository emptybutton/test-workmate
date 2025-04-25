from abc import ABC, abstractmethod
from collections.abc import Iterable, Sequence

from log_reporting.entities.report import Report


class ReportParser[ReportT: Report, LogPlaceT](ABC):
    @abstractmethod
    def parse_from(
        self, log_places: Sequence[LogPlaceT], /
    ) -> Iterable[ReportT]: ...
