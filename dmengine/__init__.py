# dmengine - calculate the results of distributed morphology analyses

"""Distributed Morphology (DM) analyses with LaTeX report output."""

__title__ = 'dmengine'
__version__ = '0.1.3'
__author__ = 'Sebastian Bank <sebastian.bank@uni-leipzig.de>'
__license__ = 'MIT, see LICENSE'
__copyright__ = 'Copyright (c) 2011-2015 Sebastian Bank'

import logging

from .analysis import Analysis
from .reporting import Report, texify

__all__ = ['Analysis', 'Report', 'calculate', 'texify']

logging.basicConfig(format='%(message)s', level=logging.INFO)


def calculate(filename, directory=None, report=False, pdf=False, view=False):
    """Return calculated DM analysis from the given config filename."""
    analysis = Analysis(filename, directory)
    analysis.calculate()
    analysis.save()

    if report or pdf or view:
        report = Report(analysis.results)
        report.save()

        if pdf or view:
            report.render(view=view)

        analysis.report = report

    return analysis
