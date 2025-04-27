from log_reporting.entities.log_level import LogLevel


def parsed_log_level_from_literal(literal: str) -> LogLevel | None:
    match literal:
        case "DEBUG":
            return LogLevel.debug
        case "INFO":
            return LogLevel.info
        case "WARNING":
            return LogLevel.warning
        case "ERROR":
            return LogLevel.error
        case "CRITICAL":
            return LogLevel.critical
        case _:
            return None
