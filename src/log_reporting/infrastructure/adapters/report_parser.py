from collections.abc import Callable, Generator, Iterable, Sequence
from dataclasses import dataclass
from functools import partial
from multiprocessing.pool import Pool
from pathlib import Path

from log_reporting.application.ports.report_parser import ReportParser
from log_reporting.entities.report import Report
from log_reporting.infrastructure.file_parsing import (
    multiprocess_parsed_file_segments,
    parsed_file_segment,
)


@dataclass
class MultiprocessReportParserFromLogFiles[ReportT: Report](
    ReportParser[ReportT, Path]
):
    pool: Pool
    divider_for_multiprocess_parsing_of_line_separators: int
    divider_for_multiprocess_parsing_of_file_segments: int
    line_separator_parsing_chunk_size: int
    generator_of_parsed_report_from_lines_: Callable[
        [], Generator[ReportT, str]
    ]

    def __post_init__(self) -> None:
        self._parsed_file_segment = partial(
            parsed_file_segment,
            generator_of_parsed_segment_line_=(
                self.generator_of_parsed_report_from_lines_
            )
        )

    def parse_from(
        self, log_file_paths: Sequence[Path], /
    ) -> Iterable[ReportT]:
        return multiprocess_parsed_file_segments(
            self.pool,
            log_file_paths,
            self.divider_for_multiprocess_parsing_of_line_separators,
            self.divider_for_multiprocess_parsing_of_file_segments,
            self.line_separator_parsing_chunk_size,
            self._parsed_file_segment,
        )


@dataclass(frozen=True)
class ReportParserFromReports[ReportT: Report](
    ReportParser[ReportT, ReportT]
):
    def parse_from(self, reports: Sequence[ReportT], /) -> Sequence[ReportT]:
        return reports
