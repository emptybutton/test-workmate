from pytest import mark

from log_reporting.entities.log_level import LogLevel
from log_reporting.infrastructure.parsed_log_level import (
    parsed_log_level_from_literal,
)


@mark.parametrize(
    "literal, result",
    [
        ["x", None],
        ["", None],
        ["DEBUG", LogLevel.debug],
        ["INFO", LogLevel.info],
        ["WARNING", LogLevel.warning],
        ["ERROR", LogLevel.error],
        ["CRITICAL", LogLevel.critical],
    ],
)
def test_parsed_log_level_from_literal(
    literal: str, result: LogLevel | None
) -> None:
    assert parsed_log_level_from_literal(literal) == result
