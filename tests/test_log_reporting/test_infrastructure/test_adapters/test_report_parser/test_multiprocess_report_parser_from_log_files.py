from multiprocessing.pool import Pool
from pathlib import Path

from _pytest.fixtures import SubRequest
from pytest import fixture

from log_reporting.entities.report import HandlerReport
from log_reporting.infrastructure.adapters.report_parser import (
    MultiprocessReportParserFromLogFiles,
)
from log_reporting.infrastructure.parsed_report import (
    generator_of_parsed_handler_report_from_lines,
)


type Parser = MultiprocessReportParserFromLogFiles[HandlerReport]


@fixture(scope="module")
def low_chunk_parser(process_pool: Pool) -> Parser:
    return MultiprocessReportParserFromLogFiles(
        pool=process_pool,
        line_separator_parsing_chunk_size=8,
        divider_for_multiprocess_parsing_of_line_separators=2,
        divider_for_multiprocess_parsing_of_file_segments=2,
        generator_of_parsed_report_from_lines_=(
            generator_of_parsed_handler_report_from_lines
        ),
    )


@fixture(scope="module")
def height_chunk_parser(process_pool: Pool) -> Parser:
    return MultiprocessReportParserFromLogFiles(
        pool=process_pool,
        line_separator_parsing_chunk_size=10_000_000,
        divider_for_multiprocess_parsing_of_line_separators=8,
        divider_for_multiprocess_parsing_of_file_segments=8,
        generator_of_parsed_report_from_lines_=(
            generator_of_parsed_handler_report_from_lines
        ),
    )


@fixture(scope="module", params=["low", "height"])
def any_parser(
    request: SubRequest,
    low_chunk_parser: Parser,
    height_chunk_parser: Parser
) -> Parser:
    match request.param:
        case "low":
            return low_chunk_parser
        case "height":
            return height_chunk_parser
        case _:
            raise ValueError


def test_any_parser_with_handler_reports(
    any_parser: Parser,
    log_path_and_log_handler_report: tuple[Path, HandlerReport],
) -> None:
    log_path, reult_report = log_path_and_log_handler_report

    reports = list(any_parser.parse_from([log_path]))

    result_report = HandlerReport.empty_report()

    for report in reports:
        result_report.expand_with(report)

    assert result_report == reult_report


def test_any_parser_with_log_handler_report_total_requests(
    any_parser: Parser,
    log_path_and_log_handler_report_total_requests: tuple[Path, int],
) -> None:
    log_path, total_requests = log_path_and_log_handler_report_total_requests

    reports = list(any_parser.parse_from([log_path]))

    result_report = HandlerReport.empty_report()

    for report in reports:
        result_report.expand_with(report)

    assert result_report.total_requests == total_requests
