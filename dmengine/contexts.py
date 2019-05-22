# contexts.py - vocabulary item insertion and rule contexts

"""Contexts for vocabulary item insertion and pre-insertion rules.

HeadContext
    ThisHead, LeftHead, RightHead, OtherHead, AnyHead, Anywhere

InsertContext
    LastInsert, AnyInsert
"""

from itertools import chain
import collections

from ._compat import map, with_metaclass

from . import features, meta, types

__all__ = ['Context', 'Contexts']


class Context(with_metaclass(meta.FactoryMeta('scope', collections.OrderedDict), object)):
    """Abstract base class and factory for contexts matching features under defined conditions."""

    Features = features.FeatureSet

    def __init__(self, features):
        self.features = self.Features(features)
        if not self.features:
            raise ValueError('%r empty features.' % self)

    def __repr__(self):
        features = str(self.features)
        return 'Context(scope=%r, features=%r)' % (self.scope, features)

    def match(self, head, left_context, right_context, up_context):
        raise NotImplementedError


class Contexts(types.Instances):
    """List of contexts created in preconfigured order."""

    new_item = Context

    def __init__(self, **kwcontexts):
        scopes = iter(self.new_item.subclasses)
        items = (self.new_item(s, kwcontexts[s])
            for s in scopes if s in kwcontexts)
        super(types.Instances, self).__init__(items)

    def items(self):
        return ((c.scope, c.features) for c in self)

    iteritems = items

    def _kwstr(self, plain=False):
        ctx = ', '.join('%s=%r' % (c.scope, str(c.features)) for c in self)
        return ctx if plain else ', %s' % ctx if ctx else ''

    def __str__(self):
        ctx = ' & '.join(map(str, self))
        return ' / %s' % ctx if ctx else ''


class HeadContext(Context):
    """Matches features on heads in the input."""


class ThisHead(HeadContext):
    """Matches the given features on the inserted-to or rule-applied head."""

    scope = 'this_head'

    def __str__(self):
        return '[__,%s]' % self.features

    def match(self, head, left_context, right_context, up_context):
        return self.features.issubset(head)


class LeftHead(HeadContext):
    """Matches the given features on the left-adjacent (inner) head."""

    scope = 'left_head'

    def __str__(self):
        return '[%s][__]' % self.features

    def match(self, head, left_context, right_context, up_context):
        return (left_context
                and any(map(self.features.issubset, left_context[-1])))


class RightHead(HeadContext):
    """Matches the given features on the right-adjacent (outer) head."""

    scope = 'right_head'

    def __str__(self):
        return '[__][%s]' % self.features

    def match(self, head, left_context, right_context, up_context):
        return (right_context
                and any(map(self.features.issubset, right_context[0])))


class OtherHead(HeadContext):
    """Matches the given features on any but the inserted-to or rule-applied head."""

    scope = 'other_head'

    def __str__(self):
        return '__...[%s]' % self.features

    def match(self, head, left_context, right_context, up_context):
        contexts = left_context + [up_context] + right_context
        other_heads = chain.from_iterable(contexts)
        return any(map(self.features.issubset, other_heads))


class AnyHead(HeadContext):
    """Matches the given features on any single head."""

    scope = 'any_head'

    def __str__(self):
        return '[%s]' % self.features

    def match(self, head, left_context, right_context, up_context):
        contexts = left_context + [[head]] + [up_context] + right_context
        all_heads = chain.from_iterable(contexts)
        return any(map(self.features.issubset, all_heads))


class Anywhere(HeadContext):
    """Matches the given features anywhere in the head structure."""

    scope = 'anywhere'

    def __str__(self):
        return '%s' % self.features

    def match(self, head, left_context, right_context, up_context):
        contexts = left_context + [[head]] + [up_context] + right_context
        all_heads = chain.from_iterable(contexts)
        all_features = self.features.from_featuresets(all_heads)
        return self.features.issubset(all_features)


class InsertContext(Context):
    """Matches features on already inserted vocabulary items in the output."""


class LastInsert(InsertContext):
    """Matches the given features on the substantial features of the last inserted vi."""

    scope = 'last_insert'

    def match(self, head, left_context, right_context, up_context):
        raise NotImplementedError


class AnyInsert(InsertContext):
    """Matches the given features on the substantial features of any inserted vi."""

    scope = 'any_insert'

    def match(self, head, left_context, right_context, up_context):
        raise NotImplementedError
