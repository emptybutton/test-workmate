from collections.abc import Generator

from log_reporting.entities.log_level_counter import LogLevelCounter
from log_reporting.entities.report import HandlerReport
from log_reporting.infrastructure.parsed_log_level import (
    parsed_log_level_from_literal,
)


def generator_of_parsed_handler_report_from_lines() -> Generator[
    HandlerReport, str
]:
    report = HandlerReport({})
    number_of_first_accessed_words = 6

    while True:
        line = (yield report)
        words = line.split()

        if len(words) < number_of_first_accessed_words:
            continue

        if words[3] != "django.request:":
            continue

        log_level = parsed_log_level_from_literal(words[2])

        if log_level is None:
            continue

        if words[4:7] == ["Internal", "Server", "Error:"]:
            endpoint = words[7]
        else:
            endpoint = words[5]

        log_level_counter = report.endpoint_map.get(endpoint)

        if log_level_counter is None:
            log_level_counter = LogLevelCounter(dict())
            report.endpoint_map[endpoint] = log_level_counter

        log_level_counter.map[log_level] += 1
