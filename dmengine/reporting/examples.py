from itertools import count


def render_example(content, *, caption=None, labelize=False):
    if labelize:
        assert not isinstance(content, list)
        label, ref = get_label()
        lines = '\n'.join(get_lines(content, caption, label))
        return lines, ref
    else:
        lines = '\n'.join(get_lines(content, caption, None))
        return lines


def get_label(*, index_counter=count(1)):
    index = next(index_counter)
    label = '\\label{ex:%d} ' % index
    reference = '\\ref{ex:%d} ' % index
    return label, reference


def get_lines(content, caption, label):
    itemize = isinstance(content, list)
    yield '\\ex.'
    if label:
        yield '\t%s' % label
    if caption:
        yield '\t\\textit{%s}%s' % (caption, '' if itemize else '\\\\')
    if content:
        if itemize:
            yield '\t\\a. %s\n' % content[0].strip().replace('\n', '\n\t')
            for c in content[1:]:
                yield '\t\\b. %s\n' % c.strip().replace('\n', '\n\t')
        else:
            yield '\t%s\n' % content.strip().replace('\n', '\n\t')
    else:
        yield ''
    yield ''
