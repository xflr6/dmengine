# outcontexts.py - readjustment contexts matching vocabulary items

"""Contexts for post-insertion readjustments.

ExponentContext
    ThisExponent, LeftExponent, RightExponent, OtherExponent

FeaturesContext
    ThisFeatures, LeftFeatures, RightFeatures, OtherFeatures
"""

from itertools import chain, imap
import collections

from . import exponents, features, meta, types

__all__ = ['ViContext', 'ViContexts']


class ViContext(object):
    """Context matching vis under defined conditions."""

    __metaclass__ = meta.FactoryMeta('scope', collections.OrderedDict)

    def match(self, vi, left_context, right_context):
        raise NotImplementedError


class ViContexts(types.Instances):
    """Output context sequence created in predetermined order."""

    new_item = ViContext

    def __init__(self, **kwcontexts):
        scopes = self.new_item.subclasses.keys()
        items = (self.new_item(s, kwcontexts[s])
            for s in scopes if s in kwcontexts)
        super(types.Instances, self).__init__(items)

    def iteritems(self):
        return ((c.scope, c.target) for c in self)

    def _kwstr(self, plain=False):
        ctx = ', '.join(c._kwstr() for c in self)
        return ctx if plain else ', %s' % ctx if ctx else ''

    def __str__(self):
        ctx = ' & '.join(imap(str, self))
        return ' / %s' % ctx if ctx else ''


class ExponentContext(ViContext):
    """Matches the vocabulary items exponent value (kind and form)."""

    Exponent = exponents.Exponent

    def __init__(self, exponent):
        self.target = self.exponent = self.Exponent(exponent)
        if not self.exponent:
            raise ValueError('%r no exponent.' % self)

    def _kwstr(self):
        return '%s=%r' % (self.scope, self.exponent.value)

    def __repr__(self):
        exponent = self.exponent.value
        return '%s(scope=%r, exponent=%r)' % (self.__class__.__base__.__name__,
            self.scope, exponent)


class ThisExponent(ExponentContext):
    """Matches the vis exponent."""

    scope = 'exponent'

    def __str__(self):
        return '%s' % self.exponent

    def match(self, vi, left_context, right_context):
        return self.exponent == vi.exponent


class LeftExponent(ExponentContext):
    """Matches the left-adjacent vis exponent."""

    scope = 'left_exponent'

    def __str__(self):
        return '%s__' % self.exponent

    def match(self, vi, left_context, right_context):
        return left_context and self.exponent == left_context[-1].exponent


class RightExponent(ExponentContext):
    """Matches the right-adjacent vis exponent."""

    scope = 'right_exponent'

    def __str__(self):
        return '__%s' % self.exponent

    def match(self, vi, left_context, right_context):
        return right_context and self.exponent == right_context[0].exponent


class OtherExponent(ExponentContext):
    """Matches any other vis exponent."""

    scope = 'other_exponent'

    def __str__(self):
        return '__...%s' % self.exponent

    def match(self, vi, left_context, right_context):
        other = chain(left_context.exponents, right_context.exponents)
        return self.exponent in other


class FeaturesContext(ViContext):
    """Matches the vocabulary items substantial features."""

    Features = features.FeatureSet

    def __init__(self, features):
        self.target = self.features = self.Features(features)
        if not self.features:
            raise ValueError('%r no features.' % self)

    def _kwstr(self):
        features = str(self.features)
        return '%s=%r' % (self.scope, features)

    def __repr__(self):
        features = str(self.features)
        return '%s(scope=%r, features=%r)' % (self.__class__.__base__.__name__,
            self.scope, features)


class ThisFeatures(FeaturesContext):
    """Matches the vis features."""

    scope = 'features'

    def __str__(self):
        return '[%s]' % self.features

    def match(self, vi, left_context, right_context):
        return self.features.issubset(vi.features)


class LeftFeatures(FeaturesContext):
    """Matches the left-adjacent vis features."""

    scope = 'left_features'

    def __str__(self):
        return '[%s]__' % self.features

    def match(self, vi, left_context, right_context):
        return (left_context
            and self.features.issubset(left_context[-1].features))


class RightFeatures(FeaturesContext):
    """Matches the right-adjacent vis exponent."""

    scope = 'right_features'

    def __str__(self):
        return '__[%s]' % self.features

    def match(self, vi, left_context, right_context):
        return (right_context
            and self.features.issubset(right_context[0].features))


class OtherFeatures(FeaturesContext):
    """Matches any other vis features."""

    scope = 'other_features'

    def __str__(self):
        return '__...[%s]' % self.features

    def match(self, vi, left_context, right_context):
        other = chain(left_context, right_context)
        return any(self.features.issubset(o.features) for o in other)
