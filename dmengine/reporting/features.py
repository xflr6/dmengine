# features.py

from .common import tabular


def render_feature(f):
    if isinstance(f, int):
        f = '%+d' % f
    return f.replace('-', '$-$')


def render_features(features, *, brackets=False):
    result = ','.join(render_feature(f) for f in features)
    if brackets:
        result = f'$[${result}$]$'
    return result


def render_number(integer):
    return f'{integer:-d}'.replace('-', '$-$')


def config_row(feature):
    value = render_feature(feature['value'])
    category = feature['category']
    name = feature['name']
    specificity = render_number(feature['specificity'])
    return (value, category, name, specificity)


def render_featureconfig(features):
    headers = ('Value', 'Category', 'Name', 'Specificity')
    table = [headers] + [config_row(f) for f in features]
    return tabular(table, cnt_content=True, cnt_table=True)
