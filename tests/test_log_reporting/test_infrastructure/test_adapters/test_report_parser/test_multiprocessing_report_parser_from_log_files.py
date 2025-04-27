from functools import partial
from multiprocessing.pool import Pool
from pathlib import Path

from pytest import fixture

from log_reporting.entities.report import HandlerReport
from log_reporting.infrastructure.adapters.report_parser import (
    MultiprocessingReportParserFromLogFiles,
)
from log_reporting.infrastructure.file_parsing import parsed_file_segment
from log_reporting.infrastructure.parsed_report import (
    generator_of_parsed_handler_report_from_lines,
)


type Parser = MultiprocessingReportParserFromLogFiles[HandlerReport]


@fixture(scope="module")
def parser(process_pool: Pool) -> Parser:
    return MultiprocessingReportParserFromLogFiles(
        pool=process_pool,
        relative_chunk_byte_count=8,
        divider_for_processes=2,
        parsed_report_from_log_file_segment=partial(
            parsed_file_segment,
            generator_of_parsed_segment_line_=(
                generator_of_parsed_handler_report_from_lines
            ),
        )
    )


def test_with_only_zero_log(parser: Parser, zero_log_path: Path) -> None:
    reports = list(parser.parse_from([zero_log_path]))

    assert reports == [HandlerReport(dict())]
