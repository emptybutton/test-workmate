from collections.abc import Iterator
from multiprocessing.pool import Pool
from pathlib import Path

from pytest import Item, fixture, mark
from pytest_asyncio import is_async_test

from log_reporting.entities.log_level import LogLevel
from log_reporting.entities.log_level_counter import LogLevelCounter
from log_reporting.entities.report import HandlerReport


@fixture(scope="session")
def app1_log_path() -> Path:
    return Path("./logs/app1.log")


@fixture(scope="session")
def app1_log_handler_report() -> HandlerReport:
    report = HandlerReport({
        "/api/v1/reviews/": LogLevelCounter({
            LogLevel.info: 7, LogLevel.error: 3
        }),
        "/api/v1/products/": LogLevelCounter({
            LogLevel.info: 4, LogLevel.error: 2
        }),
        "/admin/dashboard/": LogLevelCounter({
            LogLevel.info: 3, LogLevel.error: 1
        }),
        "/api/v1/auth/login/": LogLevelCounter({
            LogLevel.info: 5, LogLevel.error: 1
        }),
        "/admin/login/": LogLevelCounter({
            LogLevel.info: 4, LogLevel.error: 2
        }),
        "/api/v1/users/": LogLevelCounter({
            LogLevel.info: 2, LogLevel.error: 1
        }),
        "/api/v1/orders/": LogLevelCounter({
            LogLevel.info: 4, LogLevel.error: 1
        }),
        "/api/v1/support/": LogLevelCounter({
            LogLevel.info: 7, LogLevel.error: 1
        }),
        "/api/v1/cart/": LogLevelCounter({
            LogLevel.info: 5, LogLevel.error: 1
        }),
        "/api/v1/shipping/": LogLevelCounter({
            LogLevel.info: 3, LogLevel.error: 1
        }),
        "/api/v1/payments/": LogLevelCounter({
            LogLevel.info: 2
        }),
        "/api/v1/checkout/": LogLevelCounter({
            LogLevel.info: 4, LogLevel.error: 2
        }),
    })

    assert report.total_requests == 60
    return report


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
    app1_log_path: Path,
    app2_log_path: Path,
    app3_log_path: Path,
    zero_log_path: Path,
) -> tuple[Path, ...]:
    return (
        app1_log_path,
        app2_log_path,
        app3_log_path,
        zero_log_path,
    )


@fixture(scope="session")
def process_pool() -> Iterator[Pool]:
    with Pool() as pool:
        yield pool


def pytest_collection_modifyitems(items: list[Item]) -> None:
    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = mark.asyncio(loop_scope="session")

    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)
