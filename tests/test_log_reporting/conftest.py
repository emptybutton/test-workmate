from collections.abc import Iterator
from multiprocessing.pool import Pool
from pathlib import Path

from _pytest.fixtures import SubRequest
from pytest import Item, fixture, mark
from pytest_asyncio import is_async_test

from log_reporting.entities.log_level import LogLevel
from log_reporting.entities.log_level_counter import LogLevelCounter
from log_reporting.entities.report import HandlerReport


@fixture(scope="session")
def zero_log_handler_report_total_requests() -> int:
    return 0


@fixture(scope="session")
def app0_log_handler_report_total_requests() -> int:
    return 12


@fixture(scope="session")
def app1_log_handler_report_total_requests() -> int:
    return 60


@fixture(scope="session")
def app2_log_handler_report_total_requests() -> int:
    return 62


@fixture(scope="session")
def app3_log_handler_report_total_requests() -> int:
    return 66


@fixture(scope="session")
def app0_log_handler_report() -> HandlerReport:
    return HandlerReport({
        "/a": LogLevelCounter({LogLevel.info: 2}),
        "/b": LogLevelCounter({LogLevel.info: 2}),
        "/c": LogLevelCounter({LogLevel.info: 2}),
        "/d": LogLevelCounter({LogLevel.info: 2}),
        "/e": LogLevelCounter({LogLevel.info: 2}),
        "/f": LogLevelCounter({LogLevel.info: 2}),
    })


@fixture(scope="session")
def zero_log_handler_report() -> HandlerReport:
    return HandlerReport.empty_report()


@fixture(scope="session")
def app0_log_path() -> Path:
    return Path("./logs/app0.log")


@fixture(scope="session")
def app1_log_path() -> Path:
    return Path("./logs/app1.log")


@fixture(scope="session")
def app2_log_path() -> Path:
    return Path("./logs/app2.log")


@fixture(scope="session")
def app3_log_path() -> Path:
    return Path("./logs/app3.log")


@fixture(scope="session")
def zero_log_path() -> Path:
    return Path("./logs/zero.log")


@fixture(scope="session")
def log_paths(
    app0_log_path: Path,
    app1_log_path: Path,
    app2_log_path: Path,
    app3_log_path: Path,
    zero_log_path: Path,
) -> tuple[Path, ...]:
    return (
        app0_log_path,
        app1_log_path,
        app2_log_path,
        app3_log_path,
        zero_log_path,
    )


@fixture(scope="module", params=["app0", "zero"])
def log_path_and_log_handler_report(
    request: SubRequest,
    app0_log_path: Path,
    zero_log_path: Path,
    app0_log_handler_report: HandlerReport,
    zero_log_handler_report: HandlerReport,
) -> tuple[Path, HandlerReport]:
    match request.param:
        case "app0":
            return app0_log_path, app0_log_handler_report
        case "zero":
            return zero_log_path, zero_log_handler_report
        case _:
            raise ValueError


@fixture(scope="module", params=["zero", "app0", "app1", "app2", "app3"])
def log_path_and_log_handler_report_total_requests(
    request: SubRequest,
    zero_log_path: Path,
    app0_log_path: Path,
    app1_log_path: Path,
    app2_log_path: Path,
    app3_log_path: Path,
    zero_log_handler_report_total_requests: int,
    app0_log_handler_report_total_requests: int,
    app1_log_handler_report_total_requests: int,
    app2_log_handler_report_total_requests: int,
    app3_log_handler_report_total_requests: int,
) -> tuple[Path, int]:
    match request.param:
        case "zero":
            return zero_log_path, zero_log_handler_report_total_requests
        case "app0":
            return app0_log_path, app0_log_handler_report_total_requests
        case "app1":
            return app1_log_path, app1_log_handler_report_total_requests
        case "app2":
            return app2_log_path, app2_log_handler_report_total_requests
        case "app3":
            return app3_log_path, app3_log_handler_report_total_requests
        case _:
            raise ValueError


@fixture(scope="session")
def process_pool() -> Iterator[Pool]:
    with Pool() as pool:
        yield pool


def pytest_collection_modifyitems(items: list[Item]) -> None:
    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = mark.asyncio(loop_scope="session")

    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)
