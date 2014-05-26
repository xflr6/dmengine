# dmengine - calculate the results of distributed morphology analyses

"""Distributed Morphology (DM) analyses with LaTeX report output."""

__title__ = 'dmengine'
__version__ = '0.1'
__author__ = 'Sebastian Bank <sebastian.bank@uni-leipzig.de>'
__license__ = 'MIT, see LICENSE'
__copyright__ = 'Copyright (c) 2011-2014 Sebastian Bank'

import logging

logging.basicConfig(format='%(message)s', level=logging.INFO)

from .analysis import Analysis
from .reporting import Report, texify

__all__ = ['Analysis', 'Report', 'calculate', 'texify']


def calculate(filename, directory=None, report=False, pdf=False, view=False):
    """Return calculated DM analysis from the given config filename."""
    analysis = Analysis(filename, directory)
    analysis.calculate()
    analysis.save()

    if report or pdf or view:
        results = analysis.results
        analysis.report = report = Report(results)
        report.save()

        if pdf or view:
            report.render(view=view)

    return analysis


def main():
    """Execute the command-line interface."""
    import argparse

    parser = argparse.ArgumentParser(prog='dmengine',
        description='Calculates a given Distributed Morphology (DM) analysis')

    parser.add_argument('--version', action='version',
        version='%%(prog)s %s' % __version__)

    parser.add_argument('filename',
        help='dm analysis .yaml definition file')
    parser.add_argument('directory', nargs='?',
        help='analysis results output directory')

    parser.add_argument('--report', dest='report', action='store_true',
        help='create a LaTeX report from the results')
    parser.add_argument('--pdf', dest='pdf', action='store_true',
        help='render the report to PDF (implies --report)')
    parser.add_argument('--view', dest='view', action='store_true',
        help='open the report in viewer app (implies --pdf)')

    args = parser.parse_args()
    calculate(args.filename, args.directory, args.report, args.pdf, args.view)
