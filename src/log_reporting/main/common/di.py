from multiprocessing import Pool
from pathlib import Path

from log_reporting.application.generate_report import GenerateReport
from log_reporting.entities.report import HandlerReport
from log_reporting.infrastructure.adapters.report_parser import (
    MultiprocessingReportParser,
)
from log_reporting.infrastructure.report_parsing import (
    parsed_handler_report_from_log_file,
)
from log_reporting.presentation.adapters.report_views import (
    HandlerReportTablesAsReportViews,
)
from log_reporting.presentation.cli.report_view import HandlerReportTable
from log_reporting.presentation.common.di import IoCContainer


_process_pool = Pool()

_handler_report_tables_as_report_views = HandlerReportTablesAsReportViews()
_multiprocessing_handler_report_parser_from_log_files = (
    MultiprocessingReportParser(
        pool=_process_pool,
        parsed_report_from_log_place=parsed_handler_report_from_log_file,
    )
)

container = IoCContainer({
    GenerateReport[HandlerReport, Path, HandlerReportTable]: GenerateReport(
        report_parser=_multiprocessing_handler_report_parser_from_log_files,
        report_views=_handler_report_tables_as_report_views,
        report_type=HandlerReport,
    )
})
