from pathlib import Path

from log_reporting.entities.endpoint import Endpoint
from log_reporting.entities.log_level_counter import LogLevelCounter
from log_reporting.entities.report import HandlerReport
from log_reporting.infrastructure.log_level_parsing import (
    log_level_from_literal,
)


def parsed_handler_report_from_log_file(log_path: Path) -> HandlerReport:
    endpoint_map = dict[Endpoint, LogLevelCounter]()

    with log_path.open() as file:
        number_of_first_accessed_words = 6

        for line in file:
            words = line.split()

            if len(words) < number_of_first_accessed_words:
                continue

            if words[3] != "django.request:":
                continue

            log_level = log_level_from_literal(words[2])

            if log_level is None:
                continue

            if words[4:7] == ["Internal", "Server", "Error:"]:
                endpoint = words[7]
            else:
                endpoint = words[5]

            log_level_counter = endpoint_map.get(endpoint)

            if log_level_counter is None:
                log_level_counter = LogLevelCounter(dict())
                endpoint_map[endpoint] = log_level_counter

            log_level_counter.map[log_level] += 1

    return HandlerReport(endpoint_map)
