# rules.py - pre-insertion rules

"""Rules applying before insertion.

Impoverishment, Obliteration, Fission, Fusion, CopyHead, AddFeatures, Metathesis
"""

from itertools import chain, islice
import operator
import collections

from ._compat import map, iteritems, with_metaclass

from . import features, contexts, meta, types, tools

__all__ = ['Rule', 'Rules']


@meta.serializable
class Rule(with_metaclass(meta.FactoryMeta('kind'), object)):
    """Abtstract base class and factory for operations on a sequence of slots containing heads."""

    Features = features.FeatureSet
    Contexts = contexts.Contexts

    @staticmethod
    def _multi_representer(dumper, self):
        result = collections.OrderedDict(kind=self.kind)
        fields = ('features', 'this_head', 'first_head', 'second_head', 'into_first')
        result.update((f, self.__dict__[f]) for f in fields if f in self.__dict__)
        if 'contexts' in self.__dict__:
            result.update(iteritems(self.contexts))
        return dumper.represent_mapping('tag:yaml.org,2002:map', iteritems(result))

    @staticmethod
    def loop_heads(slots):
        for i_s, slot in enumerate(slots):
            for i_h, head in enumerate(slot):
                yield i_s, i_h, slot, head

    @classmethod
    def two_candidates(cls, slots):
        for i_s, i_h, slot, head in cls.loop_heads(slots):
            other = chain(islice(enumerate(slots), None, i_s), islice(enumerate(slots), i_s + 1, None))
            for o_s, other_slot in other:
                for o_h, other_head in enumerate(other_slot):
                    yield i_s, i_h, head, o_s, o_h, other_head

    def all_contexts_match(self, slots):
        for (i_s, (slot, left, right)) in enumerate(tools.curr_pred_succ(slots)):
            for (i_h, (head, up)) in enumerate(tools.curr_other(slot)):
                matching = operator.methodcaller('match', head, left, right, up)
                if all(map(matching, self.contexts)):
                    yield i_s, i_h, slot, head

    def __call__(self, slots):
        raise NotImplementedError


class Rules(types.Instances):
    """Sequence of rules to be executed before insertion."""

    new_item = Rule


class Impoverishment(Rule):
    """Delete any occurence of the fiven features on every context matching head."""

    kind = 'impoverishment'

    def __init__(self, features, **kwcontexts):
        self.features = self.Features(features)
        self.contexts = self.Contexts(**kwcontexts)
        if not self.features:
            raise ValueError('%r empty features.' % self)

    def __repr__(self):
        features = str(self.features)
        contexts = self.contexts._kwstr()
        return '%s(features=%r%s)' % (self.__class__.__name__, features, contexts)

    def __str__(self):
        return '%s -> 0%s' % (self.features, self.contexts)

    def __call__(self, slots):
        applied = False
        for i_s, i_h, slot, head in self.all_contexts_match(slots):
            if head.hascommon(self.features):
                head.remove(self.features, discard=True)
                applied = True
        return applied


class Obliteration(Rule):
    """Delete the first context matching head, if applicable delete the resulting empty slot."""

    kind = 'obliteration'

    def __init__(self, **kwcontexts):
        self.contexts = self.Contexts(**kwcontexts)
        if not self.contexts:
            raise ValueError('%r no context.' % self)

    def __repr__(self):
        contexts = self.contexts._kwstr(plain=True)
        return '%s(%s)' % (self.__class__.__name__, contexts)

    def __str__(self):
        return '[] -> 0%s' % self.contexts

    def __call__(self, slots):
        for i_s, i_h, slot, head in self.all_contexts_match(slots):
            del slot[i_h]
            if not slot:
                del slots[i_s]
            return True
        return False


class Fission(Rule):
    """Move the given features from the first context matching head to a new right-adjacent single head slot."""

    kind = 'fission'

    def __init__(self, features, this_head):
        self.this_head = self.Features(this_head)
        self.features = self.Features(features)
        if not (self.features and self.this_head):
            raise ValueError('%s empty features or this head.' % self)

    def __repr__(self):
        features = str(self.features)
        this_head = str(self.this_head)
        return '%s(features=%r, this_head=%r)' % (self.__class__.__name__,
            features, this_head)

    def __str__(self):
        return '[%s,%s...] -> [%s...][%s]' % (self.features, self.this_head,
            self.this_head, self.features)

    def __call__(self, slots):
        for i_s, i_h, slot, head in self.loop_heads(slots):
            if head.issubset(self.this_head) and head.issubset(self.features):
                head.remove(self.features)
                new_slot = slot.__class__([head.__class__(self.features)])
                slots.insert(i_s + 1, new_slot)
                return True
        return False


class Fusion(Rule):
    """Move one matching head into the slot of the other matching head."""

    kind = 'fusion'

    def __init__(self, first_head, second_head, into_first=True):
        self.first_head = self.Features(first_head)
        self.second_head = self.Features(second_head)
        self.into_first = into_first
        if not (self.first_head and self.second_head):
            raise ValueError('%r empty first or second head.' % self)

    def __repr__(self):
        first_head = str(self.first_head)
        second_head = str(self.second_head)
        into_first = '' if not self.into_first else ', into_first=False'
        return '%s(first_head=%r, second_head=%r%s)' % (self.__class__.__name__,
                                                        first_head, second_head,
                                                        into_first)

    def __str__(self):
        tmpl = '[%s]...[%s] -> '
        tmpl += '[[%s][%s]]...' if self.into_first else '...[[%s][%s]]'
        return tmpl % ((self.first_head, self.second_head) * 2)

    def __call__(self, slots):
        for i_s, i_h, head, o_s, o_h, other_head in self.two_candidates(slots):
            if self.first_head.issubset(head) and self.second_head.issubset(other_head):
                if not self.into_first:
                    i_s, i_h, o_s, o_h = o_s, o_h, i_s, i_h
                slots[i_s].extend(slots[o_s])
                del slots[o_s]
                return True
        return False


class CopyHead(Rule):
    """Copy the first context matching head to a new right-adjacent single head slot."""

    kind = 'copy'

    def __init__(self, **kwcontexts):
        self.contexts = self.Contexts(**kwcontexts)
        if not self.contexts:
            raise ValueError('%r no context.' % self)

    def __repr__(self):
        contexts = self.contexts._kwstr(plain=True)
        return '%s(%s)' % (self.__class__.__name__, contexts)

    def __str__(self):
        return '[...] -> [...][...]%s' % self.contexts

    def __call__(self, slots):
        for i_s, i_h, slot, head in self.all_contexts_match(slots):
            new_slot = slot.__class__([head.copy()])
            slots.insert(i_s + 1, new_slot)
            return True
        return False


class AddFeatures(Rule):
    """Add the given features to the first context matching head."""

    kind = 'add'

    def __init__(self, features, **kwcontexts):
        self.features = self.Features(features)
        self.contexts = self.Contexts(**kwcontexts)
        if not self.contexts:
            raise ValueError('%r no context.' % self)

    def __repr__(self):
        features = str(self.features)
        contexts = self.contexts._kwstr()
        return '%s(features=%r%s)' % (self.__class__.__name__, features,
                                      contexts)

    def __str__(self):
        return '[...] -> [...,%s]%s' % (self.features, self.contexts)

    def __call__(self, slots):
        for i_s, i_h, slot, head in self.all_contexts_match(slots):
            head.add(self.features)
            return True
        return False


class Metathesis(Rule):
    """Swap the first two slots containing matching heads."""

    kind = 'metathesis'

    def __init__(self, first_head, second_head):
        self.first_head = self.Features(first_head)
        self.second_head = self.Features(second_head)
        if not (self.first_head and self.second_head):
            raise ValueError('%r empty first or second head.' % self)

    def __repr__(self):
        first_head = str(self.first_head)
        second_head = str(self.second_head)
        return '%s(first_head=%r, second_head=%r)' % (self.__class__.__name__,
            first_head, second_head)

    def __str__(self):
        return '[%s]...[%s] -> [%s]...[%s]' % (self.first_head, self.second_head,
                                               self.second_head, self.first_head)

    def __call__(self, slots):
        for i_s, i_h, head, o_s, o_h, other_head in self.two_candidates(slots):
            if self.first_head.issubset(head) and self.second_head.issubset(other_head):
                slots[i_s], slots[o_s] = slots[o_s], slots[i_s]
                return True
        return False
