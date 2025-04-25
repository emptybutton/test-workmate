from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any


class TooLargeColumnLayoutNameError(Exception): ...


@dataclass(kw_only=True, frozen=True, slots=True)
class ColumnLayout[FieldValueT](ABC):
    name: str
    width: int

    def __post_init__(self) -> None:
        if len(self.name) > self.width:
            raise TooLargeColumnLayoutNameError

    def title(self) -> str:
        return self._filled(self.name)

    @abstractmethod
    def field(self, value: FieldValueT, /) -> str: ...

    def _filled(self, string: str) -> str:
        size_difference = self.width - len(string)

        return f"{string}{" " * size_difference}"


class FieldWithNegativeNumberError(Exception): ...


@dataclass(kw_only=True, frozen=True, slots=True)
class PositiveNumberColumnLayout(ColumnLayout[int]):
    def field(self, number: int) -> str:
        if number < 0:
            raise FieldWithNegativeNumberError

        intext_number = str(number)

        if len(intext_number) == self.width:
            return f"+{"9" * (self.width - 1)}"

        return self._filled(intext_number)


@dataclass(kw_only=True, frozen=True, slots=True)
class StringColumnLayout(ColumnLayout[str]):
    def field(self, string: str) -> str:
        if len(string) > self.width:
            return f"{string[:self.width - 3]}..."

        return self._filled(string)


class InconsistentTableSizeError(Exception): ...


@dataclass(kw_only=True, frozen=True, slots=True)
class TableLayout:
    column_separator: str = "  "
    columns: tuple[ColumnLayout[Any], ...]


def table(
    layout: TableLayout,
    rows: Sequence[Sequence[object]],
) -> str:
    table_title = layout.column_separator.join(
        column.title() for column in layout.columns
    )

    if not rows:
        return table_title

    if not all(
        len(rows[0]) == len(row)
        for row in rows
    ):
        raise InconsistentTableSizeError

    if len(rows[0]) != len(layout.columns):
        raise InconsistentTableSizeError

    lines = list[str]()

    for row in rows:
        line = layout.column_separator.join(
            layout.columns[index].field(field_value)
            for index, field_value in enumerate(row)
        )
        lines.append(line)

    return f"{table_title}\n{"\n".join(lines)}"
