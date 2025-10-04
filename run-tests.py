#!/usr/bin/env python3
# flake8: noqa

"""Run the tests with https://pytest.org."""

import pathlib
import sys

import pytest

SELF = pathlib.Path(__file__)

ARGS = [#'--verbose',
        #'--pdb',
        #'--exitfirst',  # a.k.a. -x
        #'-W', 'error',
       ]

if 'idlelib' in sys.modules:
    ARGS += ['--capture=sys', '--color=no']


print('run', [SELF.name] + sys.argv[1:])
args = ARGS + sys.argv[1:]

print(f'pytest.main({args!r})')
sys.exit(pytest.main(args))
