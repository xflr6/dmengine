"""Contexts for post-insertion readjustments matching vocabulary items.

ExponentContext
    ThisExponent, LeftExponent, RightExponent, OtherExponent

FeaturesContext
    ThisFeatures, LeftFeatures, RightFeatures, OtherFeatures
"""

import collections
from itertools import chain

from . import exponents
from . import features
from . import meta
from . import types

__all__ = ['ViContext', 'ViContexts']


class ViContext(metaclass=meta.FactoryMeta('scope', collections.OrderedDict)):  # type: ignore[metaclass]  # noqa: E501
    """Context matching vis under defined conditions."""

    def match(self, vi, left_context, right_context):
        raise NotImplementedError


class ViContexts(types.Instances):
    """Output context sequence created in predetermined order."""

    new_item = ViContext

    def __init__(self, **kwcontexts):
        scopes = iter(self.new_item.subclasses)
        items = (self.new_item(s, kwcontexts[s])
                 for s in scopes if s in kwcontexts)
        super(types.Instances, self).__init__(items)

    def items(self):
        return ((c.scope, c.target) for c in self)

    iteritems = items

    def _kwstr(self, *, plain=False):
        ctx = ', '.join(c._kwstr() for c in self)
        return ctx if plain else f', {ctx}' if ctx else ''

    def __str__(self):
        ctx = ' & '.join(map(str, self))
        return f' / {ctx}' if ctx else ''


class ExponentContext(ViContext):
    """Matches the vocabulary items exponent value (kind and form)."""

    Exponent = exponents.Exponent

    def __init__(self, exponent):
        self.target = self.exponent = self.Exponent(exponent)
        if not self.exponent:
            raise ValueError(f'{self!r} no exponent.')

    def _kwstr(self):
        return f'{self.scope}={self.exponent.value!r}'

    def __repr__(self):
        exponent = self.exponent.value
        return (f'self.__class__.__base__.__name__('
                f'scope={self.scope!r}, exponent={exponent!r})')


class ThisExponent(ExponentContext):
    """Matches the vis exponent."""

    scope = 'exponent'

    def __str__(self):
        return f'{self.exponent}'

    def match(self, vi, left_context, right_context):
        return self.exponent == vi.exponent


class LeftExponent(ExponentContext):
    """Matches the left-adjacent vis exponent."""

    scope = 'left_exponent'

    def __str__(self):
        return f'{self.exponent}__'

    def match(self, vi, left_context, right_context):
        return left_context and self.exponent == left_context[-1].exponent


class RightExponent(ExponentContext):
    """Matches the right-adjacent vis exponent."""

    scope = 'right_exponent'

    def __str__(self):
        return f'__{self.exponent}'

    def match(self, vi, left_context, right_context):
        return right_context and self.exponent == right_context[0].exponent


class OtherExponent(ExponentContext):
    """Matches any other vis exponent."""

    scope = 'other_exponent'

    def __str__(self):
        return f'__...{self.exponent}'

    def match(self, vi, left_context, right_context):
        other = chain(left_context.exponents, right_context.exponents)
        return self.exponent in other


class FeaturesContext(ViContext):
    """Matches the vocabulary items substantial features."""

    Features = features.FeatureSet

    def __init__(self, features):
        self.target = self.features = self.Features(features)
        if not self.features:
            raise ValueError(f'{self!r} no features.')

    def _kwstr(self):
        features = str(self.features)
        return f'{self.scope}={features!r}'

    def __repr__(self):
        features = str(self.features)
        return (f'self.__class__.__base__.__name__('
                f'scope={self.scope!r}, features={features!r})')


class ThisFeatures(FeaturesContext):
    """Matches the vis features."""

    scope = 'features'

    def __str__(self):
        return f'[{self.features}]'

    def match(self, vi, left_context, right_context):
        return self.features.issubset(vi.features)


class LeftFeatures(FeaturesContext):
    """Matches the left-adjacent vis features."""

    scope = 'left_features'

    def __str__(self):
        return f'[{self.features}]__'

    def match(self, vi, left_context, right_context):
        return (left_context
                and self.features.issubset(left_context[-1].features))


class RightFeatures(FeaturesContext):
    """Matches the right-adjacent vis exponent."""

    scope = 'right_features'

    def __str__(self):
        return f'__[{self.features}]'

    def match(self, vi, left_context, right_context):
        return (right_context
                and self.features.issubset(right_context[0].features))


class OtherFeatures(FeaturesContext):
    """Matches any other vis features."""

    scope = 'other_features'

    def __str__(self):
        return f'__...[{self.features}]'

    def match(self, vi, left_context, right_context):
        other = chain(left_context, right_context)
        return any(self.features.issubset(o.features) for o in other)
