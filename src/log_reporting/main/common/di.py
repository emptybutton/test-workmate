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
from log_reporting.presentation.adapters.report_views import HandlerReportViews
from log_reporting.presentation.common.di import IoCContainer


_handler_report_views = HandlerReportViews()
_multiprocessing_handler_report_parser_from_log_files = (
    MultiprocessingReportParser(
        pool=Pool(),
        parsed_report_from_log_place=parsed_handler_report_from_log_file,
    )
)

container = IoCContainer({
    GenerateReport[HandlerReport, Path, str]: GenerateReport(
        report_parser=_multiprocessing_handler_report_parser_from_log_files,
        report_views=_handler_report_views,
        report_type=HandlerReport,
    )
})
