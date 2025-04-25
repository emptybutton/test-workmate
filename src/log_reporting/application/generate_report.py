from collections.abc import Sequence
from dataclasses import dataclass

from log_reporting.application.ports.report_parser import ReportParser
from log_reporting.application.ports.report_views import ReportViews
from log_reporting.entities.report import Report


@dataclass(kw_only=True, frozen=True, slots=True)
class GenerateReport[ReportT: Report, LogPlaceT, ReportViewT]:
    report_parser: ReportParser[ReportT, LogPlaceT]
    report_views: ReportViews[ReportT, ReportViewT]
    report_type: type[ReportT]

    def __call__(self, log_places: Sequence[LogPlaceT]) -> ReportViewT:
        parsed_reports = self.report_parser.parse_from(log_places)

        result_report = self.report_type.empty_report()

        for parsed_report in parsed_reports:
            result_report.expand_with(parsed_report)

        return self.report_views.report_view(result_report)
