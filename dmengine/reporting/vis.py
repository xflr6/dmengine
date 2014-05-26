# vis.py

import re
from itertools import izip

from .examples import render_example
from .features import render_features
from .contexts import render_contexts

SUBSCRIPT = re.compile(r'/(\d+)')

VI = '/%s/\t$\\leftrightarrow$\t%s%s'


def render_exponent(exponent, regex=SUBSCRIPT):
    return regex.sub(r'\\textsubscript{\1}', exponent)


def render_vi(vi, tmpl=VI):
    exponent = render_exponent(vi['exponent'])
    features = render_features(vi['features'], brackets=True)
    context = render_contexts(vi)
    return tmpl % (exponent, features, context)


def render_vis(vis):
    example_refs = (render_example(render_vi(vi), labelize=True)
        for vi in vis)
    examples, refs = izip(*example_refs)
    for vi, ref in izip(vis, refs):
        vi['ref'] = ref
    return ''.join(examples)
