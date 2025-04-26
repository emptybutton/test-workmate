from collections.abc import Sequence
from typing import NewType

from log_reporting.presentation.cli.table import (
    PositiveNumberColumnLayout,
    StringColumnLayout,
    TableLayout,
    table,
)


HandlerReportTable = NewType("HandlerReportTable", str)
handler_report_table_layout = TableLayout(
    column_separator=" ",
    columns=(
        StringColumnLayout(name="HANDLER", width=23),
        PositiveNumberColumnLayout(name="DEBUG", width=7),
        PositiveNumberColumnLayout(name="INFO", width=7),
        PositiveNumberColumnLayout(name="WARNING", width=7),
        PositiveNumberColumnLayout(name="ERROR", width=7),
        PositiveNumberColumnLayout(name="CRITICAL", width=8),
    )
)


def handler_report_table(
    total_requests: int,
    rows: Sequence[tuple[str, int, int, int, int, int]]
) -> HandlerReportTable:
    return HandlerReportTable(
        f"Total requests: {total_requests}"
        + f"\n\n{table(handler_report_table_layout, rows)}"
    )
