from dataclasses import dataclass

from log_reporting.application.ports.report_views import ReportViews
from log_reporting.entities.log_level import LogLevel
from log_reporting.entities.report import HandlerReport, Report, XyzReport
from log_reporting.presentation.cli.report_view import (
    HandlerReportTable,
    XyzReportLines,
    handler_report_table,
    xyz_report_lines,
)


class InvalidTableLayoutError(Exception): ...


@dataclass(frozen=True)
class HandlerReportTablesAsReportViews(
    ReportViews[HandlerReport, HandlerReportTable]
):
    def report_view(self, report: HandlerReport, /) -> HandlerReportTable:
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

        return handler_report_table(report.total_requests, rows)


@dataclass(frozen=True)
class ReportsAsReportViews[ReportT: Report](ReportViews[ReportT, ReportT]):
    def report_view(self, report: ReportT, /) -> ReportT:
        return report


@dataclass(frozen=True)
class XyzReportLinesAsReportViews(ReportViews[XyzReport, XyzReportLines]):
    def report_view(self, report: XyzReport, /) -> XyzReportLines:
        return xyz_report_lines(report.x, report.y, report.z)
