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
        min_slice_count = len(delimeter_offsets) // self.divider_for_processes

        if min_slice_count <= 1:
            return [cast("slice[int, int, None]", slice(0, None))]

        slice_delimeter_offset_batches = batched(
            delimeter_offsets, min_slice_count, strict=False
        )

        file_slices: list["slice[int, int | None, None]"] = [  # noqa: UP037
            cast(
                "slice[int, int, None]",
                slice(
                    slice_delimeter_offsets[0] + 1, slice_delimeter_offsets[-1]
                ),
            )
            for slice_delimeter_offsets in slice_delimeter_offset_batches
        ]
        file_slices.extend((
            cast("slice[int, int, None]", slice(0, delimeter_offsets[0])),
            cast(
                "slice[int, int, None]", slice(delimeter_offsets[-1] + 1, None)
            ),
        ))

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
