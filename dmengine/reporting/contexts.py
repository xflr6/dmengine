# contexts.py

import collections

from .common import translate
from .features import render_features

CONTEXTS = collections.OrderedDict((key, translate(tmpl)) for key, tmpl in [
    ('this_head', '[__,%s]'),
    ('left_head', '[%s][__]'),
    ('right_head', '[__][%s]'),
    ('other_head', '__...[%s]'),
    ('any_head', '[%s]'),
    ('anywhere', '%s'),
])

EXPCONTEXTS = collections.OrderedDict((key, translate(tmpl)) for key, tmpl in [
    ('exponent', '%s'),
    ('left_exponent', '%s__'),
    ('right_exponent', '__%s'),
    ('other_exponent', '__...%s'),
    ('features', '%s'),
    ('left_features', '%s__'),
    ('right_features', '__%s'),
    ('other_features', '__...%s'),
])


def render_contexts(item):
    if not any(key in item for key in CONTEXTS):
        return ''
    return ' $/$ %s' % ' \\& '.join(tmpl % render_features(item[key])
        for key, tmpl in CONTEXTS.iteritems() if key in item)


def render_expcontexts(item):
    if not any(key in item for key in EXPCONTEXTS):
        return ''
    return ' $/$ %s' % ' \\& '.join(tmpl % item[key]
        for key, tmpl in EXPCONTEXTS.iteritems() if key in item)
