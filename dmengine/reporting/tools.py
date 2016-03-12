# tools.py

import os
import sys
import contextlib
from itertools import tee

from .._compat import zip, zip_longest

__all__ = ['pairwise', 'grouper', 'swapext', 'chdir', 'current_path']


def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def grouper(n, iterable, fillvalue=None):
    return zip_longest(*[iter(iterable)] * n, fillvalue=fillvalue)


def swapext(filename, extension, delimiter='.'):
    f_name, f_delim, f_ext = filename.rpartition(delimiter)
    return '%s%s%s' % (f_name, f_delim, extension)


@contextlib.contextmanager
def chdir(path):
    """Change the current working directory, restore on context exit."""
    if not path:
        try:
            yield
        finally:
            pass
        return

    oldwd = os.getcwd()
    os.chdir(path)
    try:
        yield path
    finally:
        os.chdir(oldwd)


def current_path(*names):
    """Return the path to names relative to the current module."""
    depth = 0 if __name__ == '__main__' else 1

    frame = sys._getframe(depth)

    try:
        path = os.path.dirname(frame.f_code.co_filename)
    finally:
        del frame

    if names:
        path = os.path.join(path, *names)

    return os.path.realpath(path)
