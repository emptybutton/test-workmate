import os
from functools import partial
from multiprocessing import Pool
from pathlib import Path

from log_reporting.application.generate_report import GenerateReport
from log_reporting.entities.report import HandlerReport
from log_reporting.infrastructure.adapters.report_parser import (
    MultiprocessingReportParserFromLogFiles,
)
from log_reporting.infrastructure.file_parsing import parsed_file_segment
from log_reporting.infrastructure.parsed_report import (
    generator_of_parsed_handler_report_from_lines,
)
from log_reporting.presentation.adapters.report_views import (
    HandlerReportTablesAsReportViews,
)
from log_reporting.presentation.cli.report_view import HandlerReportTable
from log_reporting.presentation.common.di import IoCContainer


_process_pool = Pool()

_parsed_handler_report_from_log_file_segment = partial(
    parsed_file_segment,
    generator_of_parsed_segment_line_=(
        generator_of_parsed_handler_report_from_lines
    ),
)

_handler_report_tables_as_report_views = HandlerReportTablesAsReportViews()
_multiprocessing_handler_report_parser_from_log_files = (
    MultiprocessingReportParserFromLogFiles(
        pool=_process_pool,
        relative_chunk_byte_count=2_000_000,
        divider_for_processes=(os.process_cpu_count() or 1) * 2,
        parsed_report_from_log_file_segment=(
            _parsed_handler_report_from_log_file_segment
        ),
    )
)

container = IoCContainer()
container.provide(
    GenerateReport(
        report_parser=_multiprocessing_handler_report_parser_from_log_files,
        report_views=_handler_report_tables_as_report_views,
        report_type=HandlerReport,
    ),
    provides=GenerateReport[HandlerReport, Path, HandlerReportTable],
)
container.on_close(_process_pool.close)
