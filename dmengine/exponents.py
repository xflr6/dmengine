"""Exponents: Prefix, Stem, Suffix."""

import operator

from . import meta
from . import types

__all__ = ['Exponent', 'ExponentList']


class ExponentMeta(type):
    """Pick and verify Prefix/Stem/Suffix by hypen position in value."""

    def __call__(self, value):  # noqa: N804
        if isinstance(value, self):
            return value

        if self.kind:
            if '-' in value:
                raise ValueError
            form = value
            value = self._template.format(form)
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

        return super().__call__(value, form)


@meta.serializable
class Exponent(metaclass=ExponentMeta):
    """Prefix, stem, and suffix identified by value hyphen-position."""

    kind: str | None = None

    @staticmethod
    def _multi_representer(dumper, self):
        return dumper.represent_scalar('tag:yaml.org,2002:str', str(self.value))

    def __init__(self, value, form):
        self.value = value
        self.form = form
        if not form:
            raise ValueError(f'{self!r} empty form.')

    def copy(self, *, form=None):
        if form is None:
            form = self.form
        return self.__class__(form)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.form!r})'

    def __str__(self):
        return f'/{self.value}/'

    def __eq__(self, other):
        return (isinstance(other, Exponent)
                and self.kind == other.kind and self.value == other.value)

    def __ne__(self, other):
        return not self == other


class ExponentList(types.List):
    """List of exponents sortable by kind (prefix < stem < suffix)."""

    sortkey = operator.attrgetter('_sortslot')

    def __str__(self):
        return ' '.join(map(str, self))

    @property
    def spellout(self):
        exponents = sorted(self, key=self.sortkey)
        return ''.join(e.value for e in exponents)


class Prefix(Exponent):
    """Prefix, trailing hyphen."""

    kind = 'prefix'

    _template = '{}-'

    _sortslot = -1


class Stem(Exponent):
    """Stem, no hyphen."""

    kind = 'stem'

    _template = '{}'

    _sortslot = 0


class Suffix(Exponent):
    """Suffix, leading hyphen."""

    kind = 'suffix'

    _template = '-{}'

    _sortslot = 1
