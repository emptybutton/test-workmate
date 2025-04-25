import sys
from io import TextIOBase
from typing import cast

from log_reporting.main.common.di import container
from log_reporting.presentation.cli.cli import Cli


cli = Cli(
    container,
    output_file=cast(TextIOBase, sys.stdout),
    entrypoint_commands=("report-logs", ),
)
