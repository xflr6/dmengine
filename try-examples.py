#!/usr/bin/env python3

import glob

import dmengine

EXAMPLES = 'examples/*.yaml'

DIRECTORY = 'examples-output'

PDF = True


for filename in glob.glob(EXAMPLES):
    analysis = dmengine.calculate(filename, directory=DIRECTORY, pdf=PDF)
