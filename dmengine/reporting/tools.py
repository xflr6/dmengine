import itertools
import os
import sys

__all__ = ['grouper', 'swapext', 'current_path']


def grouper(n, iterable, *, fillvalue=None):
    return itertools.zip_longest(*[iter(iterable)] * n, fillvalue=fillvalue)


def swapext(filename, extension, *, delimiter: str = '.') -> str:
    (f_name, f_delim, _) = filename.rpartition(delimiter)
    return f'{f_name}{f_delim}{extension}'


def current_path(*names: os.PathLike[str] | str) -> str:
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
