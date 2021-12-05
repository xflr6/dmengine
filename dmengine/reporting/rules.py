from .common import translate
from .contexts import render_contexts
from .examples import render_example
from .features import render_features

MAP = {}


def render_rules(rules):
    if not rules:
        return ''
    example_refs = (render_example(MAP[r['kind']](r), labelize=True)
                    for r in rules)
    examples, refs = zip(*example_refs)
    for r, ref in zip(rules, refs):
        r['ref'] = ref
    return ''.join(examples)


def register(func):
    MAP[func.__name__] = func
    return func


@register
def impoverishment(rule, *, tmpl=translate('%s -> \\0%s')):
    return tmpl % (render_features(rule['features']), render_contexts(rule))


@register
def obliteration(rule, *, tmpl=translate('[] -> \\0%s')):
    return tmpl % render_contexts(rule)


@register
def fission(rule, *, tmpl=translate('[%s,%s...] -> [%s...][%s]')):
    features = render_features(rule['features'])
    this_head = render_features(rule['this_head'])
    return tmpl % (features, this_head, this_head, features)


@register
def fusion(rule):
    tmpl = '[%s]...[%s] -> '
    if rule['into_first']:
        tmpl += '[[%s][%s]]...'
    else:
        tmpl += '...[[%s][%s]]'
    tmpl = translate(tmpl)
    first_head = render_features(rule['first_head'])
    second_head = render_features(rule['second_head'])
    return tmpl % (first_head, second_head, first_head, second_head)


@register
def copy(rule, *, tmpl=translate('[...] -> [...][...]%s')):
    return tmpl % render_contexts(rule)


@register
def add(rule, *, tmpl=translate('[...] -> [...,%s]%s')):
    return tmpl % (render_features(rule['features']), render_contexts(rule))


@register
def metathesis(rule, *, tmpl=translate('[%s]...[%s] -> [%s]...[%s]')):
    first_head = render_features(rule['first_head'])
    second_head = render_features(rule['second_head'])
    return tmpl % (first_head, second_head, second_head, first_head)
