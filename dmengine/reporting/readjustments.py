from .common import translate
from .contexts import render_expcontexts
from .examples import render_example

MAP = {}


def render_readjustments(readjustments):
    if not readjustments:
        return ''
    examples_refs = (render_example(MAP[r['kind']](r), labelize=True)
                     for r in readjustments)
    examples, refs = zip(*examples_refs)
    for r, ref in zip(readjustments, refs):
        r['ref'] = ref
    return ''.join(examples)


def register(func):
    MAP[func.__name__] = func
    return func


@register
def delete(read, *, tmpl=translate('%s -> \\0%s')):
    return tmpl % (read['exponent'], render_expcontexts(read))


@register
def copy(read, *, tmpl=translate('%s -> %s %s%s')):
    exponent = read['exponent']
    contexts = render_expcontexts(read)
    return tmpl % (exponent, exponent, exponent, contexts)


@register
def metathesis(read, *, tmpl=translate('%s...%s-> %s...%s')):
    first_exponent = read['first_exponent']
    second_exponent = read['second_exponent']
    return tmpl % (first_exponent, second_exponent,
                   second_exponent, first_exponent)


@register
def transform(read, *, tmpl=translate('%s $\\sim$> %s%s')):
    search = read['search']
    replace = read['replace'].replace('\\', '\\textbackslash')
    contexts = render_expcontexts(read)
    return tmpl % (search, replace, contexts)
