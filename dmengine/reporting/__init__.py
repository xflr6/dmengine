"""Create LaTeX reports from analysis results YAML file and render to PDF."""

from .report import Report

__all__ = ['Report', 'texify']


def texify(filename=None, *,
           pdf: bool = False, view: bool = False) -> Report:
    report = Report(filename)
    report.save()

    if pdf or view:
        report.render(view=view)

    return report
