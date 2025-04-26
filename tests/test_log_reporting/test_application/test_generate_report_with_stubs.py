from pytest import fixture

from log_reporting.application.generate_report import GenerateReport
from log_reporting.entities.log_level import LogLevel
from log_reporting.entities.log_level_counter import LogLevelCounter
from log_reporting.entities.report import HandlerReport
from log_reporting.infrastructure.adapters.report_parser import (
    ReportParserFromReports,
)
from log_reporting.presentation.adapters.report_views import (
    ReportsAsReportViews,
)


type Operation = GenerateReport[HandlerReport, HandlerReport, HandlerReport]


@fixture(scope="module")
def operation() -> Operation:
    return GenerateReport(
        report_parser=ReportParserFromReports(),
        report_views=ReportsAsReportViews(),
        report_type=HandlerReport,
    )


def test_result_without_log_places(operation: Operation) -> None:
    result = operation(tuple())

    assert result == HandlerReport(endpoint_map=dict())


def test_result_with_one_log_place(operation: Operation) -> None:
    result = operation([HandlerReport(endpoint_map=dict())])

    assert result == HandlerReport(endpoint_map=dict())


def test_result_with_many_log_places(operation: Operation) -> None:
    result = operation([
        HandlerReport({
            "/x/": LogLevelCounter({LogLevel.info: 3, LogLevel.error: 10}),
            "/y/": LogLevelCounter({LogLevel.debug: 30, LogLevel.info: 2}),
        }),
        HandlerReport({
            "/y/": LogLevelCounter({LogLevel.info: 3, LogLevel.error: 30}),
            "/z/": LogLevelCounter({LogLevel.critical: 50}),
        }),
    ])

    assert result == HandlerReport({
        "/x/": LogLevelCounter({LogLevel.info: 3, LogLevel.error: 10}),
        "/y/": LogLevelCounter({
            LogLevel.debug: 30, LogLevel.info: 5, LogLevel.error: 30
        }),
        "/z/": LogLevelCounter({LogLevel.critical: 50}),
    })
