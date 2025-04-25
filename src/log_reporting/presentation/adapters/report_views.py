from dataclasses import dataclass

from log_reporting.application.ports.report_views import ReportViews
from log_reporting.entities.log_level import LogLevel
from log_reporting.entities.report import HandlerReport
from log_reporting.presentation.cli.table import (
    PositiveNumberColumnLayout,
    StringColumnLayout,
    TableLayout,
    table,
)


class InvalidTableLayoutError(Exception): ...


@dataclass
class HandlerReportViews(ReportViews[HandlerReport, str]):
    def __post_init__(self) -> None:
        self._table_layout = TableLayout(
            column_separator=" ",
            columns=(
                StringColumnLayout(name="HANDLER", width=23),
                PositiveNumberColumnLayout(name="DEBUG", width=7),
                PositiveNumberColumnLayout(name="INFO", width=7),
                PositiveNumberColumnLayout(name="WARNING", width=7),
                PositiveNumberColumnLayout(name="ERROR", width=7),
                PositiveNumberColumnLayout(name="CRITICAL", width=8),
            )
        )

    def report_view(self, report: HandlerReport, /) -> str:
        rows = tuple(
            (
                endpoint,
                log_level_counter.map[LogLevel.debug],
                log_level_counter.map[LogLevel.info],
                log_level_counter.map[LogLevel.warning],
                log_level_counter.map[LogLevel.error],
                log_level_counter.map[LogLevel.critical],
            )
            for endpoint, log_level_counter in report.endpoint_map.items()
        )

        return (
            f"Total requests: {report.total_requests}"
            f"\n\n{table(self._table_layout, rows)}"
        )
