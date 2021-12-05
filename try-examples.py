#!/usr/bin/env python3

import glob
import pathlib
import sys

import dmengine

SELF = pathlib.Path(__file__)

EXAMPLES = 'examples/*.yaml'

DIRECTORY = 'examples-output'

PDF = True


print('run', [SELF.name] + sys.argv[1:])
for filename in glob.glob(EXAMPLES):
    print()
    print(f'dmengine.calculate({filename!r}, directory={DIRECTORY!r}, pdf={PDF!r})')
    analysis = dmengine.calculate(filename, directory=DIRECTORY, pdf=PDF)
