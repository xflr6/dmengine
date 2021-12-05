"""Entry-point for the dmengine command-line interface."""

import argparse
import os
import sys

from . import __version__, calculate

__all__ = ['main']


def main():
    """Execute the command-line interface."""
    parser = argparse.ArgumentParser(prog='dmengine',
        description='Calculates a given Distributed Morphology (DM) analysis')

    parser.add_argument('--version', action='version',
                        version='%%(prog)s %s' % _version())

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
    calculate(args.filename, args.directory,
              args.report, args.pdf, args.view)


def _version():
    pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return f'{__version__} from {pkg_dir} (python {sys.version[:3]})'


if __name__ == '__main__':
    main()
