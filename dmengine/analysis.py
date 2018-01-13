# analysis.py - load, calculate, save

"""Load an analysis config file, calculate it, and save the results."""

import io
import collections
import logging

from ._compat import map

import yaml

from . import features, vis, rules, readjustments, calculation, types, tools

__all__ = ['Analysis']

log = logging.getLogger()


class Analysis(object):
    """Distibuted Morphology (DM) analyis from YAML configuration file."""

    Features = features.FeatureSystem

    Vis = vis.VocabularyItems

    Rules = rules.Rules

    Readjustments = readjustments.Readjustments

    Calculator = calculation.Calculator

    def __init__(self, filename, directory=None, encoding='utf-8'):
        self.filename = filename
        self.results = tools.derive_filename(filename, '-results', 'yaml', directory)

        log.info('%r' % self)

        with io.open(self.filename, encoding=encoding) as fd:
            cfg = yaml.safe_load(fd)

        self.author = cfg.get('author', 'Anomymous')
        self.title = cfg.get('title', 'DM-Analyis')

        self.features = self.Features(cfg['features'], always_bag=cfg.get('multisets'))

        self.vis = self.Vis(cfg['vis'])

        self.rules = self.Rules(cfg.get('rules', []))

        self.readjustments = self.Readjustments(cfg.get('readjustments', []))

        self.paradigms = [collections.OrderedDict([
            ('name', p['name']),
            ('headers', types.FlowList(p['headers'])),
            ('inputs', list(map(types.FlowList, p['inputs']))),
            ('spellouts_expected', types.List(p.get('spellouts_expected', []))),
        ]) for p in cfg['paradigms']]

        inputs = (i for p in self.paradigms for i in p['inputs'])
        self.inputs = list(map(SlotList.from_heads, inputs))

        self.calculator = self.Calculator(cfg.get('insertion', 'cyclic'),
            self.inputs, self.rules, self.vis, self.readjustments)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.filename)

    def calculate(self):
        log.info('\tcalculate..')
        self.worklog, self.outputs, self.spellouts = self.calculator()

    def save(self, encoding='utf-8', newline=''):
        log.info('\tsave to %r..' % self.results)

        data = collections.OrderedDict([
            ('author', self.author),
            ('title', self.title),
            ('insertion', self.calculator.insertion.kind),
            ('multisets', self.features.always_bag),
            ('features', self.features),
            ('vis', self.vis),
            ('rules', self.rules),
            ('readjustments', self.readjustments),
            ('paradigms', self.paradigms),
            ('worklog', self.worklog),
        ])

        with io.open(self.results, 'w', encoding=encoding, newline=newline) as fd:
            yaml.dump(data, fd)


class SlotList(types.FlowList):
    """Hierarchy of potentially fused heads represented as sequence."""

    @classmethod
    def from_heads(cls, heads):
        return cls(Slot([Head(h)]) for h in heads)

    def __str__(self):
        return '%s' % ' '.join(map(str, self))


class Slot(types.List):
    """Sequence of heads that have been fused."""

    def __str__(self):
        return '#%s#' % ' '.join(map(str, self))


class Head(features.FeatureSet):
    """Head (morpheme, lexical item) as a (multi)set of morphosyntactic features."""

    def __str__(self):
        return '[%s]' % super(Head, self).__str__()
