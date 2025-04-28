from collections import defaultdict
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from itertools import batched
from multiprocessing.pool import Pool
from pathlib import Path
from typing import Any, cast

from log_reporting.application.ports.report_parser import ReportParser
from log_reporting.entities.report import Report
from log_reporting.infrastructure.file_parsing import (
    parsed_file_line_delimeter_offsets,
)
from log_reporting.infrastructure.lang_tools import UnpackingCall, slices


@dataclass(frozen=True)
class MultiprocessingReportParserFromLogFiles[ReportT: Report](
    ReportParser[ReportT, Path]
):
    pool: Pool
    relative_chunk_byte_count: int
    divider_for_processes: int
    parsed_report_from_log_file_segment: Callable[
        [Path, "slice[int, int | None, None]"], ReportT
    ]

    def parse_from(
        self, log_file_paths: Sequence[Path], /
    ) -> Iterable[ReportT]:
        arg_packs = tuple(
            (
                log_file_path,
                slice_,
                self.relative_chunk_byte_count,
            )
            for log_file_path in log_file_paths
            for slice_ in slices(self._file_segment_range(log_file_path))
        )

        delimeter_offset_batch_and_file_path = self.pool.map(
            _parsed_file_line_delimeter_offsets_and_file_paths, arg_packs
        )

        delimeter_offset_batch_by_file_path = defaultdict[Path, list[int]](list)

        for delimeter_offset_batch, log_path in (
            delimeter_offset_batch_and_file_path
        ):
            delimeter_offset_batch_by_file_path[log_path].extend(
                delimeter_offset_batch
            )

        arg_packs = tuple(
            (log_path, slice_)
            for log_path, delimeter_offset_batch in (
                delimeter_offset_batch_by_file_path.items()
            )
            for slice_ in self._file_slices(delimeter_offset_batch)
        )

        return self.pool.map(
            UnpackingCall(self.parsed_report_from_log_file_segment),
            arg_packs,
        )

    def _file_slices(
        self, delimeter_offsets: list[int]
    ) -> list["slice[int, int | None, None]"]:
        batch_size = len(delimeter_offsets) // self.divider_for_processes

        if batch_size == 0:
            batch_size = 1

        slice_delimeter_offset_batches = tuple(batched(
            delimeter_offsets, batch_size, strict=False
        ))

        file_slices = list["slice[int, int | None, None]"]()
        prevous_delimeter_offset_bacth: tuple[int, ...] = (-1, )

        for index, delimeter_offset_bacth in enumerate(
            slice_delimeter_offset_batches
        ):
            is_batch_last = index == len(slice_delimeter_offset_batches) - 1

            start = prevous_delimeter_offset_bacth[-1] + 1
            stop = None if is_batch_last else delimeter_offset_bacth[-1]

            slice_ = cast(
                "slice[int, int | None, None]",
                slice(start, stop),
            )
            file_slices.append(slice_)
            prevous_delimeter_offset_bacth = delimeter_offset_bacth

        return file_slices

    def _file_segment_range(self, file_path: Path) -> range:
        return range(
            0,
            file_path.stat().st_size,
            file_path.stat().st_size // self.divider_for_processes or 1,
        )


def _parsed_file_line_delimeter_offsets_and_file_paths(
    args: tuple[Path, "slice[int, int, Any]", int]
) -> tuple[list[int], Path]:
    return parsed_file_line_delimeter_offsets(*args), args[0]


@dataclass(frozen=True)
class ReportParserFromReports[ReportT: Report](
    ReportParser[ReportT, ReportT]
):
    def parse_from(self, reports: Sequence[ReportT], /) -> Sequence[ReportT]:
        return reports
