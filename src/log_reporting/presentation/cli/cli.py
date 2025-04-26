import sys
from dataclasses import dataclass, field
from io import TextIOBase
from pathlib import Path

from log_reporting.application.generate_report import GenerateReport
from log_reporting.entities.report import HandlerReport, Report
from log_reporting.presentation.cli.report_view import HandlerReportTable
from log_reporting.presentation.common.di import IoCContainer


@dataclass(frozen=True)
class ReportSpec:
    report_type: type[Report]
    report_view_type: type[str]


@dataclass
class Cli:
    container: IoCContainer
    output_file: TextIOBase
    entrypoint_commands: tuple[str, ...]
    _report_spec_by_report_name: dict[str, ReportSpec] = field(init=False)

    def __post_init__(self) -> None:
        self._report_spec_by_report_name = {
            "handlers": ReportSpec(HandlerReport, HandlerReportTable),
        }

    def __call__(self) -> None:
        if "--help" in sys.argv or "-h" in sys.argv or len(sys.argv) == 1:
            self._help()
            return

        if "--report" in sys.argv and "-r" in sys.argv:
            self._print(self._error_message("both -r and --report specified"))
            return

        if "--report" not in sys.argv and "-r" not in sys.argv:
            self._print(self._error_message("-r or --report are not specified"))
            return

        if "--report" in sys.argv:
            report_name_option_index = sys.argv.index("--report")
            report_name_option = "--report"
        else:
            report_name_option_index = sys.argv.index("-r")
            report_name_option = "-r"

        try:
            report_name = sys.argv[report_name_option_index + 1]
        except IndexError:
            self._print(self._error_message(
                f"{report_name_option} value are not specified"
            ))
            sys.exit(1)

        report_spec = self._report_spec_by_report_name.get(report_name)

        if report_spec is None:
            self._print(
                self._error_message(f"invalid {report_name_option} values")
                + "\n"
                + self._tip_message(f"valid {report_name_option} values: ")
                + " ".join(self._report_spec_by_report_name)
            )
            sys.exit(1)

        paths = tuple(
            Path(arg)
            for index, arg in enumerate(sys.argv)
            if index not in {
                0, report_name_option_index, report_name_option_index + 1
            }
        )

        for path in paths:
            if not path.is_file():
                self._print(self._error_message(f"{path} is not a file"))
                sys.exit(1)

        generate_report = self.container.get(
            GenerateReport[
                report_spec.report_type,  # type: ignore[name-defined]
                Path,
                report_spec.report_view_type  # type: ignore[name-defined]
            ]
        )

        report_veiw = generate_report(paths)
        self._print(report_veiw)

    def _error_message(self, string: str) -> str:
        return f"[error] {string}"

    def _tip_message(self, string: str) -> str:
        return f"[tip] {string}"

    def _help(self) -> None:
        self._print(
            "\nApplication for analyzing and generating log reports."
            + "\n\nUsage: "
            + " ".join(self.entrypoint_commands)
            + " [OPTIONS] [LOG_PATHS]"
            + "\n\nOptions:"
            + "\n-r, --report <REPORT_NAME>       Name of a report to generate"
            + "\n-h, --help                       Display this message"
        )

    def _print(self, text: str) -> None:
        print(text, file=self.output_file)
