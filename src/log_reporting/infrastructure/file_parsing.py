from collections import defaultdict
from collections.abc import Callable, Generator, Sequence
from itertools import batched
from multiprocessing.pool import Pool
from pathlib import Path
from typing import Any, cast

from log_reporting.infrastructure.lang_tools import UnpackingCall, slices


type FileSegment = "slice[int, int | None, Any]"  # noqa: TC008


def parsed_file_line_count(file_path: Path, file_chunk_size: int) -> int:
    with file_path.open("rb") as file:
        parsed_file_line_count = 0
        reading_file_chunk = file.read(file_chunk_size)

        while reading_file_chunk:
            parsed_file_line_count += reading_file_chunk.count(b"\n")
            reading_file_chunk = file.read(file_chunk_size)

        return parsed_file_line_count


def parsed_file_line_separator_offsets(
    file_path: Path,
    file_segment: FileSegment,
    most_right_delimiter_every_bytes: int,
) -> list[int]:
    parsed_file_line_separator_offsets_ = list[int]()
    reading_file_chunk_size = most_right_delimiter_every_bytes

    with file_path.open("rb") as file:
        offset = file_segment.start
        file.seek(offset)

        file_segment_stop = file_segment.stop or file_path.stat().st_size

        while offset < file_segment_stop:
            reading_file_chunk = file.read(min((
                reading_file_chunk_size,
                file_segment_stop - offset - 1,
            )))

            if not reading_file_chunk:
                break

            try:
                index = reading_file_chunk.rindex(b"\n")
            except ValueError:
                ...
            else:
                parsed_file_line_separator_offsets_.append(index + offset)

            offset += len(reading_file_chunk)

        return parsed_file_line_separator_offsets_


def parsed_file_segment[T](
    file_path: Path,
    file_segment: FileSegment,
    generator_of_parsed_segment_line_: Callable[[], Generator[T, str]],
) -> T:
    generator_of_parsed_segment_line = generator_of_parsed_segment_line_()

    with file_path.open() as file:
        file.seek(file_segment.start)
        offset_of_parsed_lines = file_segment.start

        result = next(generator_of_parsed_segment_line)

        for line in file:
            offset_of_parsed_lines += len(line.encode())

            result = generator_of_parsed_segment_line.send(line)

            segment_ended = (
                file_segment.stop is not None
                and offset_of_parsed_lines >= file_segment.stop
            )
            if segment_ended:
                break

        return result


def multiprocess_parsed_file_segments[ParsedFileSegmentT](  # noqa: PLR0917
    pool: Pool,
    file_paths: Sequence[Path],
    divider_for_multiprocess_parsing_of_line_separators: int,
    divider_for_multiprocess_parsing_of_file_segments: int,
    line_separator_parsing_chunk_size: int,
    parsed_file_segment: Callable[[Path, FileSegment], ParsedFileSegmentT],
) -> list[ParsedFileSegmentT]:
    arg_packs = tuple(
        (
            file_path,
            slice_,
            line_separator_parsing_chunk_size,
        )
        for file_path in file_paths
        for slice_ in slices(file_segment_range(
            file_path, divider_for_multiprocess_parsing_of_line_separators
        ))
    )

    line_separator_offset_batch_and_file_path = pool.map(
        _parsed_file_line_separator_offsets_and_file_paths, arg_packs
    )

    line_separator_offset_batch_by_file_path = defaultdict[Path, list[int]](
        list
    )
    for line_separator_offset_batch, log_path in (
        line_separator_offset_batch_and_file_path
    ):
        line_separator_offset_batch_by_file_path[log_path].extend(
            line_separator_offset_batch
        )

    arg_packs = tuple(
        (log_path, slice_)
        for log_path, line_separator_offset_batch in (
            line_separator_offset_batch_by_file_path.items()
        )
        for slice_ in file_segments(
            line_separator_offset_batch,
            divider_for_multiprocess_parsing_of_file_segments,
        )
    )
    return pool.map(UnpackingCall(parsed_file_segment), arg_packs)


def _parsed_file_line_separator_offsets_and_file_paths(
    args: tuple[Path, "slice[int, int, Any]", int]
) -> tuple[list[int], Path]:
    return parsed_file_line_separator_offsets(*args), args[0]


def file_segments(
    line_separator_offsets: list[int],
    divider: int,
) -> list[FileSegment]:
    batch_size = len(line_separator_offsets) // divider

    if batch_size == 0:
        batch_size = 1

    slice_line_separator_offset_batches = tuple(batched(
        line_separator_offsets, batch_size, strict=False
    ))

    file_slices = list[FileSegment]()
    prevous_line_separator_offset_bacth: tuple[int, ...] = (-1, )

    for index, line_separator_offset_bacth in enumerate(
        slice_line_separator_offset_batches
    ):
        is_batch_last = index == len(slice_line_separator_offset_batches) - 1

        start = prevous_line_separator_offset_bacth[-1] + 1
        stop = None if is_batch_last else line_separator_offset_bacth[-1]

        slice_ = cast(FileSegment, slice(start, stop))
        file_slices.append(slice_)
        prevous_line_separator_offset_bacth = line_separator_offset_bacth

    return file_slices


def file_segment_range(file_path: Path, divider: int) -> range:
    return range(
        0,
        file_path.stat().st_size,
        file_path.stat().st_size // divider or 1,
    )
