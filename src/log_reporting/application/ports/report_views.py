from abc import ABC, abstractmethod

from log_reporting.entities.report import Report


class ReportViews[ReportT: Report, ReportView](ABC):
    @abstractmethod
    def report_view(self, report: ReportT, /) -> ReportView: ...
