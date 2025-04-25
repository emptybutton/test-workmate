from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from multiprocessing.pool import Pool

from log_reporting.application.ports.report_parser import ReportParser
from log_reporting.entities.report import Report


@dataclass(frozen=True)
class MultiprocessingReportParser[ReportT: Report, LogPlaceT](
    ReportParser[ReportT, LogPlaceT]
):
    pool: Pool
    parsed_report_from_log_place: Callable[[LogPlaceT], ReportT]

    def parse_from(
        self, log_places: Sequence[LogPlaceT], /
    ) -> Iterable[ReportT]:
        return self.pool.map(self.parsed_report_from_log_place, log_places)
