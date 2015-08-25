# exponents.py - prefix, stem, suffix

"""Prefix, Stem, Suffix."""

from itertools import imap
import operator

from . import meta, types

__all__ = ['Exponent', 'ExponentList']


class ExponentMeta(type):
    """Pick and verify Prefix/Stem/Suffix by hypen position in value."""

    def __call__(self, value):
        if isinstance(value, self):
            return value

        if self.kind:
            if '-' in value:
                raise ValueError
            form = value
            value = self._template % form
        elif value.count('-') > 1:
            raise ValueError
        elif value.startswith('-'):
            self = Suffix
            form = value[1:]
        elif value.endswith('-'):
            self = Prefix
            form = value[:-1]
        elif '-' not in value:
            self = Stem
            form = value
        else:
            raise ValueError

        return super(ExponentMeta, self).__call__(value, form)


@meta.serializable
class Exponent(object):
    """Prefix, stem, and suffix identified by value hyphen-position."""

    __metaclass__ = ExponentMeta

    kind = None

    @staticmethod
    def _multi_representer(dumper, self):
        return dumper.represent_scalar('tag:yaml.org,2002:str', self.value)

    def __init__(self, value, form):
        self.value = value
        self.form = form
        if not form:
            raise ValueError('%r empty form.' % self)

    def copy(self, form=None):
        if form is None:
            form = self.form
        return self.__class__(form)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.form)

    def __unicode__(self):
        return u'/%s/' % self.value

    def __str__(self):
        return unicode(self).encode('ascii', 'backslashreplace')

    def __eq__(self, other):
        return (isinstance(other, Exponent) and
            self.kind == other.kind and self.value == other.value)

    def __ne__(self, other):
        return not self == other


class ExponentList(types.List):
    """List of exponents sortable by kind (prefix < stem < suffix)."""

    sortkey = operator.attrgetter('_sortslot')

    def __str__(self):
        return ' '.join(imap(str, self))

    @property
    def spellout(self):
        exponents = sorted(self, key=self.sortkey)
        return ''.join(e.value for e in exponents)


class Prefix(Exponent):
    """Prefix, trailing hyphen."""

    kind = 'prefix'

    _template = '%s-'

    _sortslot = -1


class Stem(Exponent):
    """Stem, no hyphen."""

    kind = 'stem'

    _template = '%s'

    _sortslot = 0


class Suffix(Exponent):
    """Suffix, leading hyphen."""

    kind = 'suffix'

    _template = '-%s'

    _sortslot = 1
