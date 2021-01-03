#!/usr/bin/env python
# run-tests.py

import sys

import pytest

ARGS = [
    #'--exitfirst',
    #'--pdb',
]

if 'idlelib' in sys.modules:
    ARGS.extend(['--capture=sys', '--color=no'])

sys.exit(pytest.main(ARGS + sys.argv[1:]))
