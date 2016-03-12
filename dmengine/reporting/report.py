# report.py

import io
import string
import logging

import yaml

from . import pdflatex, tools

from .features import render_featureconfig
from .vis import render_vis
from .rules import render_rules
from .readjustments import render_readjustments
from .paradigms import paradigms, input_paradigms, input_paradigms_processed
from .log import render_log

__all__ = ['Report']

log = logging.getLogger()


class Report(object):
    """LaTeX source from DM analyis results YAML file."""

    template = tools.current_path('template.tex')

    def __init__(self, analysis, filename=None, pdfname=None, encoding='utf-8'):
        self.analysis = analysis
        if filename is None:
            filename = tools.swapext(analysis, 'tex')
        self.filename = filename
        if pdfname is None:
            pdfname = tools.swapext(analysis, 'pdf')
        self.pdfname = pdfname

        log.info('%r' % self)

        with io.open(self.analysis, encoding=encoding) as fd:
            analysis = yaml.safe_load(fd)

        log.info('\tcreate..')
        self.sections = {
            'AUTHOR': analysis['author'],
            'TITLE': analysis['title'],
            'FEATURES': render_featureconfig(analysis['features']),
            'VOCABULARY_ITEMS': render_vis(analysis['vis']),
            'RULES': render_rules(analysis['rules']),
            'READJUSTMENTS': render_readjustments(analysis['readjustments']),
            'OUTPUTS': paradigms(analysis['paradigms'], analysis['worklog']),
            'INPUTS': input_paradigms(analysis['paradigms']),
            'INPUTS_PROCESSED': input_paradigms_processed(analysis['paradigms'],
                analysis['worklog']),
        }

        if analysis['insertion'] != 'flat':
            self.sections['LOG'] = render_log(analysis['paradigms'],
                analysis['worklog'], analysis['rules'], analysis['readjustments'])
        else:
            self.sections['LOG'] = ''

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.analysis)

    def save(self, encoding='utf-8', newline=''):
        log.info('\tsave to %r..' % self.filename)
        with io.open(self.template, encoding=encoding) as fd:
            template = fd.read()

        template = string.Template(template)
        document = template.safe_substitute(self.sections)

        with io.open(self.filename, 'w', encoding=encoding, newline=newline) as fd:
            fd.write(document)

    def render(self, view=False):
        log.info('\trender to %r..' % self.pdfname)
        pdflatex.render(self.filename, view=view)
