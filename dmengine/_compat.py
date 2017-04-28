# _compat.py - Python 2/3 compatibility

import os
import sys

PY2 = sys.version_info[0] == 2


if PY2:  # pragma: no cover
    text_type = unicode
    string_types = basestring

    range = xrange

    apply = apply

    def itervalues(d):
        return d.itervalues()

    def iteritems(d):
        return d.iteritems()

    from itertools import imap as map, izip as zip, ifilter as filter,\
        izip_longest as zip_longest

    def py3_unicode_to_str(cls):
        return cls

    def makedirs(name, mode=0o777, exist_ok=False):
        try:
            os.makedirs(name, mode)
        except OSError:
            if not exist_ok or not os.path.isdir(name):
                raise


else:  # pragma: no cover
    text_type = string_types = str

    range = range

    def apply(f, *args, **kwargs):
        return f(*args, **kwargs)

    def itervalues(d):
        return iter(d.values())

    def iteritems(d):
        return iter(d.items())

    map, zip, filter = map, zip, filter
    from itertools import zip_longest

    def py3_unicode_to_str(cls):
        cls.__str__ = cls.__unicode__
        del cls.__unicode__
        return cls

    makedirs = os.makedirs


def with_metaclass(meta, *bases):
    """From Jinja2 (BSD licensed).

    https://github.com/mitsuhiko/jinja2/blob/master/jinja2/_compat.py
    """
    class metaclass(meta):
        __call__ = type.__call__
        __init__ = type.__init__
        def __new__(cls, name, this_bases, d):
            if this_bases is None:
                return type.__new__(cls, name, (), d)
            return meta(name, bases, d)
    return metaclass('temporary_class', None, {})
