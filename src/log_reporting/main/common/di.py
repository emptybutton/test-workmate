import os
from multiprocessing import Pool
from pathlib import Path

from log_reporting.application.generate_report import GenerateReport
from log_reporting.entities.report import HandlerReport
from log_reporting.infrastructure.adapters.report_parser import (
    MultiprocessReportParserFromLogFiles,
)
from log_reporting.infrastructure.parsed_report import (
    generator_of_parsed_handler_report_from_lines,
)
from log_reporting.presentation.adapters.report_views import (
    HandlerReportTablesAsReportViews,
)
from log_reporting.presentation.cli.report_view import HandlerReportTable
from log_reporting.presentation.common.di import IoCContainer


_process_pool = Pool()
_cpu_count = os.process_cpu_count() or 1

_handler_report_tables_as_report_views = HandlerReportTablesAsReportViews()

_multiprocess_handler_report_parser_from_log_files = (
    MultiprocessReportParserFromLogFiles(
        pool=_process_pool,
        line_separator_parsing_chunk_size=4_000_000,
        divider_for_multiprocess_parsing_of_line_separators=_cpu_count,
        divider_for_multiprocess_parsing_of_file_segments=_cpu_count * 4,
        generator_of_parsed_report_from_lines_=(
            generator_of_parsed_handler_report_from_lines
        ),
    )
)

container = IoCContainer()
container.provide(
    GenerateReport(
        report_parser=_multiprocess_handler_report_parser_from_log_files,
        report_views=_handler_report_tables_as_report_views,
        report_type=HandlerReport,
    ),
    provides=GenerateReport[HandlerReport, Path, HandlerReportTable],
)
container.on_close(_process_pool.close)
