from collections.abc import Callable, Generator
from pathlib import Path
from typing import Any


def parsed_file_line_count(file_path: Path, file_chunk_size: int) -> int:
    with file_path.open("rb") as file:
        parsed_file_line_count = 0
        reading_file_chunk = file.read(file_chunk_size)

        while reading_file_chunk:
            parsed_file_line_count += reading_file_chunk.count(b"\n")
            reading_file_chunk = file.read(file_chunk_size)

        return parsed_file_line_count


def parsed_file_line_delimeter_offsets(
    file_path: Path,
    file_segment: "slice[int, int, Any]",
    most_right_delimiter_every_bytes: int,
) -> list[int]:
    parsed_file_line_delimeter_offsets_ = list[int]()
    reading_file_chunk_size = most_right_delimiter_every_bytes

    with file_path.open("rb") as file:
        offset = file_segment.start
        file.seek(offset)

        reading_file_chunk = file.read(min((
            reading_file_chunk_size,
            file_segment.stop - offset - 1,
        )))

        while reading_file_chunk and offset < file_segment.stop:
            try:
                index = reading_file_chunk.rindex(b"\n")
            except ValueError:
                ...
            else:
                parsed_file_line_delimeter_offsets_.append(index + offset)

            reading_file_chunk = file.read(min((
                reading_file_chunk_size,
                file_segment.stop - offset - 1,
            )))
            offset += len(reading_file_chunk)

        return parsed_file_line_delimeter_offsets_


def parsed_file_segment[T](
    file_path: Path,
    slice: "slice[int, int | None]",
    generator_of_parsed_segment_line_: Callable[[], Generator[T, str]],
) -> T:
    generator_of_parsed_segment_line = generator_of_parsed_segment_line_()
    with file_path.open() as file:
        file.seek(slice.start)
        offset_of_parsed_lines = slice.start

        result = next(generator_of_parsed_segment_line)

        for line in file:
            offset_of_parsed_lines += len(line.encode())

            if slice.stop is not None and offset_of_parsed_lines >= slice.stop:
                break

            result = generator_of_parsed_segment_line.send(line)

        return result
