import sys

from log_reporting.main.cli.__main__ import main  # noqa: PLC2701


def test_ok() -> None:
    sys.argv[:] = ["_", "./logs/app1.log", "-r", "handlers"]
    main()
