import contextlib
from itertools import tee, zip_longest
import os
import sys

__all__ = ['pairwise', 'grouper', 'swapext', 'chdir', 'current_path']


def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def grouper(n, iterable, *, fillvalue=None):
    return zip_longest(*[iter(iterable)] * n, fillvalue=fillvalue)


def swapext(filename, extension, *, delimiter='.'):
    f_name, f_delim, _ = filename.rpartition(delimiter)
    return f'{f_name}{f_delim}{extension}'


@contextlib.contextmanager
def chdir(path):
    """Change the current working directory, restore on context exit."""
    if not path:
        yield
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
