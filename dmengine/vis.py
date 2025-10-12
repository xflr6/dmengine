"""Vocabulary items: exponent, features, contexts (match against slot, sort by specificity)."""

import collections
import functools
from itertools import groupby
import operator

from . import contexts
from . import exponents
from . import features
from . import meta
from . import tools
from . import types

__all__ = ['VocabularyItem', 'VocabularyItems', 'ViList']


@meta.serializable
class VocabularyItem(object):
    """Holds the exponent, its substantial features, and other contexts for insertion."""

    Exponent = exponents.Exponent

    Features = features.FeatureSet

    Contexts = contexts.Contexts

    @staticmethod
    def _representer(dumper, self):
        result = collections.OrderedDict([('exponent', self.exponent),
                                          ('features', self.features)])
        result.update(self.contexts.items())
        return dumper.represent_mapping('tag:yaml.org,2002:map', result.items())

    def __init__(self, exponent, features, **kwcontexts):
        self.exponent = self.Exponent(exponent)
        self.features = self.Features(features)
        self.contexts = self.Contexts(**kwcontexts)
        if not self.features:
            raise ValueError(f'{self!r} empty features.')

    def copy(self, *, form=None):
        exponent = self.exponent.copy(form=form)
        features = self.features.values
        contexts = {ctx.scope: ctx.features.values for ctx in self.contexts}
        return self.__class__(exponent, features, **contexts)

    def __repr__(self):
        contexts = self.contexts._kwstr()
        return (f'{self.__class__.__name__}('
                f'exponent={self.exponent.value!r},'
                f' features={str(self.features)!r}{contexts})')

    def __str__(self):
        return f'{self.exponent} <-> {self.features}{self.contexts}'

    def match(self, head, left_context, right_context, up_context):
        matching = operator.methodcaller('match', head,
                                         left_context, right_context,
                                         up_context)
        return (self.features.issubset_visible(head)
                and all(map(matching, self.contexts)))

    @functools.cached_property
    def specificity(self):
        mueller_specificity = tuple(map(len, self.features.by_specificity))
        return mueller_specificity + (sum(len(c.features) for c in self.contexts),)


class VocabularyItems(types.Instances):
    """Sequence of vocabulary items to be used in insertion."""

    new_item = VocabularyItem

    def filter(self, predicate=None):
        return ViList(filter(predicate, self) if predicate is not None else self)

    def matching(self, head, left_context, right_context, up_context):
        matching = operator.methodcaller('match', head,
                                         left_context, right_context,
                                         up_context)
        return self.filter(matching)

    # TODO: finish this
    def matching_(self, slot, left_context, right_context):
        return Matching((head, vi)
            for head, up_context in tools.curr_other(slot)
            for vi in filter(
                operator.methodcaller('match', head, left_context, right_context, up_context),
                self))


class ViList(types.List):
    """List of vocabulary items sortable by specifity."""

    ExponentList = exponents.ExponentList

    sortkey = operator.attrgetter('specificity')

    def __str__(self):
        return ' '.join(map(str, (vi.exponent for vi in self)))

    def sort(self, *, key=sortkey, reverse=True):
        super().sort(key=key, reverse=reverse)

    def by_specificty(self, *, sortkey=sortkey, reverse=True):
        vis = sorted(self, key=sortkey, reverse=reverse)
        return [self.__class__(g) for k, g in groupby(vis, sortkey)]

    @property
    def most_specific(self, *, sortkey=sortkey):
        vis = sorted(self, key=sortkey, reverse=True)
        return next(self.__class__(g) for k, g in groupby(vis, sortkey))

    @property
    def exponents(self):
        return self.ExponentList(vi.exponent for vi in self)


class Matching(types.StarInstances):

    new_item = collections.namedtuple('Match', ['head', 'vi'])  # type: ignore[name-match]  # noqa: E501

    sortkey = lambda m: m.vi.specificity  # noqa: E731

    def sort(self, *, key=sortkey, reverse=True):
        super().sort(key=key, reverse=reverse)

    @property
    def most_specific(self, *, sortkey=sortkey):
        matches = sorted(self, key=sortkey, reverse=True)
        return next(self.__class__(g) for k, g in groupby(matches, sortkey))

    def as_dicts(self):
        return [{'head': m.head.values_visible, 'matching': m.vi} for m in self]
