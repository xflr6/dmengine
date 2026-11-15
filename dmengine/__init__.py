# dmengine - calculate the results of distributed morphology analyses

"""Distributed Morphology (DM) analyses with LaTeX report output."""

import logging

from .analysis import Analysis
from .reporting import Report, texify

__all__ = ['Analysis', 'Report', 'calculate', 'texify']

__title__ = 'dmengine'
__version__ = '0.4.2.dev0'
__author__ = 'Sebastian Bank <sebastian.bank@uni-leipzig.de>'
__license__ = 'MIT, see LICENSE.txt'
__copyright__ = 'Copyright (c) 2011-2025 Sebastian Bank'


logging.basicConfig(format='%(message)s', level=logging.INFO)


def calculate(filename, *, directory=None,
              report: bool = False,
              pdf: bool = False,
              view: bool = False) -> Analysis:
    """Return calculated DM analysis from the given config filename."""
    analysis = Analysis(filename, directory=directory)
    analysis.calculate()
    analysis.save()
    if report or pdf or view:
        analysis.report = Report(analysis.results)
        analysis.report.save()
        if pdf or view:
            analysis.report.render(view=view)
    return analysis
