from log_reporting.main.cli.cli import cli
from log_reporting.main.common.di import container


def main() -> None:
    try:
        cli()
    finally:
        container.close()


if __name__ == "__main__":
    main()
