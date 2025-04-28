from _pytest.fixtures import SubRequest
from pytest import fixture

from log_reporting.entities.report import HandlerReport
from log_reporting.presentation.adapters.report_views import (
    HandlerReportTablesAsReportViews,
)
from log_reporting.presentation.cli.report_view import HandlerReportTable


type Views = HandlerReportTablesAsReportViews


@fixture(scope="module")
def views() -> Views:
    return HandlerReportTablesAsReportViews()


@fixture(scope="module", params=["app0", "zero"])
def handler_report_and_its_view(
    request: SubRequest,
    app0_log_handler_report: HandlerReport,
    zero_log_handler_report: HandlerReport,
) -> tuple[HandlerReport, HandlerReportTable]:
    match request.param:
        case "zero":
            return (
                zero_log_handler_report,
                HandlerReportTable("Total requests: 0"),
            )
        case "app0":
            return (
                app0_log_handler_report,
                HandlerReportTable(
                    "HANDLER                 DEBUG   INFO    WARNING ERROR   CRITICAL"  # noqa: E501
                    "\n/a                      0       2       0       0       0       "  # noqa: E501
                    "\n/b                      0       2       0       0       0       "  # noqa: E501
                    "\n/c                      0       2       0       0       0       "  # noqa: E501
                    "\n/d                      0       2       0       0       0       "  # noqa: E501
                    "\n/e                      0       2       0       0       0       "  # noqa: E501
                    "\n/f                      0       2       0       0       0       "  # noqa: E501
                    "\n\nTotal requests: 12"
                ),
            )
        case _:
            raise ValueError


def test_view_of_handler_report(
    views: Views,
    handler_report_and_its_view: tuple[HandlerReport, HandlerReportTable],
) -> None:
    report, expected_view = handler_report_and_its_view
    view = views.report_view(report)

    assert view == expected_view
