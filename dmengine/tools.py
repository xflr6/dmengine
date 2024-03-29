"""Generic re-useable functions."""

from collections.abc import Sequence
import os

__all__ = ['uniqued', 'curr_pred_succ', 'curr_other', 'derive_filename']


def uniqued(iterable):
    seen = set()
    add = seen.add
    return [i for i in iterable if i not in seen and not add(i)]


def curr_pred_succ(iterable):
    if not isinstance(iterable, Sequence):
        iterable = tuple(iterable)
    for i, item in enumerate(iterable):
        yield item, iterable[:i], iterable[i + 1:]


def curr_other(iterable):
    if not isinstance(iterable, Sequence):
        iterable = tuple(iterable)
    for i, item in enumerate(iterable):
        yield item, iterable[:i] + iterable[i + 1:]


def derive_filename(filename, *, suffix=None, extension=None, directory=None):
    assert suffix or extension

    if directory:
        filename = os.path.basename(filename)

    name, delim, ext = filename.partition('.')
    if suffix:
        name += suffix
    if extension:
        ext = extension
    filename = f'{name}{delim}{ext}'

    if directory:
        os.makedirs(directory, exist_ok=True)
        filename = os.path.join(directory, filename)

    return filename
