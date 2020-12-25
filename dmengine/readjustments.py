# readjustments.py - post-insertion readjustment rules

"""Readjustment rules applying after insertion.

DeleteExponent, CopyExponent, MetatheseExponents, TransformExponent
"""

import collections
from itertools import permutations
import operator
import re

from ._compat import map, iteritems, with_metaclass

from . import exponents
from . import meta
from . import outcontexts
from . import tools
from . import types

__all__ = ['Readjustment', 'Readjustments']


@meta.serializable
class Readjustment(with_metaclass(meta.FactoryMeta('kind'), object)):
    """Abtstract base class and factory for post-insertion operations on a vi sequence."""

    Exponent = exponents.Exponent

    Contexts = outcontexts.ViContexts

    @staticmethod
    def _multi_representer(dumper, self):
        result = collections.OrderedDict(kind=self.kind)
        fields = ('exponent', 'first_exponent', 'second_exponent', 'search', 'replace')
        result.update((f, self.__dict__[f]) for f in fields if f in self.__dict__)
        if 'contexts' in self.__dict__:
            result.update(iteritems(self.contexts))
        return dumper.represent_mapping('tag:yaml.org,2002:map', iteritems(result))

    def __init__(self, exponent, **kwcontexts):
        self.exponent = self.Exponent(exponent)
        self.contexts = self.Contexts(**kwcontexts)

    def __repr__(self):
        exponent = self.exponent.value
        contexts = self.contexts._kwstr()
        return '%s(exponent=%r%s)' % (self.__class__.__name__, exponent, contexts)

    def all_contexts_and_exp_match(self, vis):
        for i, (vi, left, right) in enumerate(tools.curr_pred_succ(vis)):
            matching = operator.methodcaller('match', vi, left, right)
            if self.exponent == vi.exponent and all(map(matching, self.contexts)):
                yield i, vi

    def all_contexts_match(self, vis):
        for i, (vi, left, right) in enumerate(tools.curr_pred_succ(vis)):
            matching = operator.methodcaller('match', vi, left, right)
            if all(map(matching, self.contexts)):
                yield i, vi

    def __call__(self, vis):
        raise NotImplementedError


class Readjustments(types.Instances):
    """Sequence of readjustments to be executed after insertion."""

    new_item = Readjustment


class DeleteExponent(Readjustment):
    """Delete the first matching exponents vi."""

    kind = 'delete'

    def __str__(self):
        return '%s -> 0%s' % (self.exponent, self.contexts)

    def __call__(self, vis):
        for i, vi in self.all_contexts_and_exp_match(vis):
            del vis[i]
            return True
        return False


class CopyExponent(Readjustment):
    """Copy the first matching exponents vi to the right-adjacent position."""

    kind = 'copy'

    def __str__(self):
        return '%s -> %s %s%s' % (self.exponent, self.exponent, self.exponent,
                                  self.contexts)

    def __call__(self, vis):
        for i, vi in self.all_contexts_and_exp_match(vis):
            vis.insert(i + 1, vi.copy())
            return True
        return False


class MetatheseExponents(Readjustment):
    """Swap the first two matching exponents vis."""

    kind = 'metathesis'

    def __init__(self, first_exponent, second_exponent):
        self.first_exponent = self.Exponent(first_exponent)
        self.second_exponent = self.Exponent(second_exponent)

    def __repr__(self):
        first = self.first_exponent.value
        second = self.second_exponent.value
        tmpl = '%s(first_exponent=%r, second_exponent=%r)'
        return tmpl % (self.__class__.__name__, first, second)

    def __str__(self):
        return '%s...%s-> %s...%s' % (self.first_exponent, self.second_exponent,
                                      self.second_exponent, self.first_exponent)

    def __call__(self, vis):
        fe, se = self.first_exponent, self.second_exponent
        for ((f_i, first), (s_i, second)) in permutations(enumerate(vis), 2):
            if first.exponent == fe and second.exponent == se:
                vis[f_i], vis[s_i] = vis[s_i], vis[f_i]
                return True
        return False


class TransformExponent(Readjustment):
    """Search and replace the given regexes in the exponent form of all matching vis."""

    kind = 'transform'

    def __init__(self, search, replace, **kwcontexts):
        self.search = search
        self.replace = replace
        self.contexts = self.Contexts(**kwcontexts)
        self._subn = re.compile(search).subn

    def __repr__(self):
        contexts = self.contexts._kwstr()
        return '%s(search=%r, replace=%r%s)' % (self.__class__.__name__,
                                                self.search, self.replace,
                                                contexts)

    def __str__(self):
        return '%s ~> %s%s' % (self.search, self.replace, self.contexts)

    def __call__(self, vis):
        applied = False
        for i, vi in self.all_contexts_match(vis):
            new_form, subbed = self._subn(self.replace, vi.exponent.form)
            applied = True
            if subbed:
                vis[i] = vi.copy(new_form)
        return applied
