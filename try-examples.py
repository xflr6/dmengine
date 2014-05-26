#!/usr/bin/env python
# try-examples.py

import glob

import dmengine

EXAMPLES = 'examples/*.yaml'
DIRECTORY = 'examples-output'
PDF = True


for filename in glob.glob(EXAMPLES):
    analysis = dmengine.calculate(filename, DIRECTORY, pdf=PDF)
