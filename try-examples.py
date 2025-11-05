#!/usr/bin/env python3

import glob
import pathlib
import sys

import dmengine

EXAMPLES = 'examples/*.yaml'

DIRECTORY = 'examples-output'

PDF = False


print('run', [pathlib.Path(__file__).name] + sys.argv[1:])

for filename in glob.glob(EXAMPLES):
    print('', f'dmengine.calculate({filename!r}, directory={DIRECTORY!r}, pdf={PDF!r})', sep='\n')
    analysis = dmengine.calculate(filename, directory=DIRECTORY, pdf=PDF)
