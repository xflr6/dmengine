# features.py - sets and bags of morphosyntactic features

"""Sets and multisets of predefined feature values."""

from itertools import chain, groupby
import operator
import collections

from ._compat import PY2, string_types, apply, map, itervalues, with_metaclass

import oset

from . import meta, tools

__all__ = ['FeatureSystem', 'FeatureSet', 'FeatureBag']


# TODO: refactor this module

class FeatureMeta(type):
    """Retrieve from last created feature system as default."""

    system = None

    def __call__(self, value=None):
        if value:
            key = self.system.get_key(value)
            self = self.system.mapping[key]
        return super(FeatureMeta, self).__call__()


class Feature(with_metaclass(FeatureMeta, object)):
    """Hideable morphosyntactic feature."""

    __slots__ = ('visible',)

    def __init__(self, visible=True):
        self.visible = visible

    def __nonempty__(self):
        return self.visible

    def __eq__(self, other):
        return self.__class__ is other.__class__

    def __ne__(self, other):
        return self.__class__ is not other.__class__

    def __hash__(self):
        return hash(self.__class__)

    def __repr__(self):
        hidden = '' if self.visible else 'hidden '
        category = ' ' + self.category if self.category else ''
        return '<%s%s%s feature>' % (hidden, self.value, category)

    def __str__(self):
        return self.value if self.visible else '_%s_' % self.value

    def hide(self):
        if not self.visible:
            raise ValueError('Unable to hide %r.' % self)
        self.visible = False


class FeatureSetMeta(type):

    system = None

    def __call__(self, values, sortkey=operator.attrgetter('index')):
        if isinstance(values, self):
            return values.copy()

        if isinstance(values, string_types):
            values = values.replace(',', ' ').split()
        keys = map(self.system.get_key, values)
        features = map(apply, map(self.system.mapping.__getitem__, keys))
        features = sorted(features, key=sortkey)
        return super(FeatureSetMeta, self).__call__(features)


@meta.serializable
class FeatureSet(with_metaclass(FeatureSetMeta, object)):
    """Ordered set of morphosyntactic features."""

    features = oset.oset

    @staticmethod
    def _multi_representer(dumper, self):
        return dumper.represent_sequence('tag:yaml.org,2002:seq', self.values)

    @classmethod
    def from_features(cls, features):
        return super(cls.__class__, cls).__call__(features)

    @classmethod
    def from_featuresets(cls, featuresets):
        features = chain.from_iterable(fs.features for fs in featuresets)
        return cls.from_features(features)

    def __init__(self, features):
        self.features = self.features(features)

    def copy(self):
        return self.from_features(f.__class__() for f in self.features)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, ' '.join(self.values))

    def __str__(self):
        return ' '.join(map(str, self.features))

    def __nonzero__(self):
        return bool(self.features)

    def __len__(self):
        return len(self.features)

    def issubset(self, other):
        return self.features <= other.features

    def issubset_visible(self, other):
        return self.features <= other.visible

    def hascommon(self, other):
        return not self.features.isdisjoint(other.features)

    def _clearlazy(self):
        attrs = self.__dict__
        for name in ('values', 'visible', 'values_visible'):
            if name in attrs:
                del attrs[name]

    @meta.lazyproperty
    def values(self):
        return [f.value for f in self.features]

    @meta.lazyproperty
    def visible(self):
        return self.features.__class__(f for f in self.features if f.visible)

    @meta.lazyproperty
    def values_visible(self):
        return [f.value for f in self.features if f.visible]

    @property
    def by_category(self, groupkey=operator.attrgetter('category')):
        features = sorted(self.features, key=groupkey)
        mapping = {k: [f.value for f in g]
            for k, g in groupby(features, groupkey)}
        return [mapping.get(c, []) for c in self.__class__.system.categories]

    @property
    def by_specificity(self, groupkey=operator.attrgetter('specificity')):
        features = sorted(self.features, key=groupkey)
        mapping = {k: [f.value for f in g]
            for k, g in groupby(features, groupkey)}
        return [mapping.get(c, []) for c in self.__class__.system.specificities]

    def add(self, other):
        self._clearlazy()
        self.features |= other.features

    def remove(self, other, discard=False):
        if not discard and not other.features <= self.features:
            raise KeyError
        self._clearlazy()
        self.features -= other.features

    def consume(self, other):
        if not other.features <= self.features:
            raise KeyError
        self._clearlazy()
        for f in other.features & self.features:
            f.hide()


class FeatureBag(FeatureSet):
    """Ordered bag of morphosyntactic features."""

    features = list

    def issubset(self, other):
        return all(map(other.features.__contains__, self.features))

    def issubset_visible(self, other):
        return all(map(other.visible.__contains__, self.features))

    def hascommon(self, other):
        return any(map(other.features.__contains__, self.features))

    def add(self, other):
        self._clearlazy()
        self.features += other.features

    def remove(self, other, discard=False):
        if not discard and not self.issubset(other):
            raise KeyError
        self._clearlazy()
        if discard:
            for f in other.features:
                try:
                    self.features.remove(f)
                except ValueError:
                    pass
        else:
            for f in other.features:
                self.features.remove(f)

    def consume(self, other):
        if not self.issubset(other):
            raise KeyError
        self._clearlazy()
        for f in other.features:
            for s in self.features:
                if s == f and s.visible:
                    s.hide()
                    break
            else:
                raise ValueError


class FeatureSet(FeatureSet):
    """Ordered set or bag of morphosyntactic features."""


@meta.serializable
class FeatureSystem(object):
    """Collection of defined morphosyntactic features values."""

    Feature = Feature

    FeatureSet = FeatureSet

    FeatureBag = FeatureBag

    @staticmethod
    def _representer(dumper, self):
        result = [collections.OrderedDict([
            ('value', f.value),
            ('category', f.category),
            ('specificity', f.specificity),
            ('name', f.name)])
            for f in itervalues(self.mapping)]
        return dumper.represent_sequence('tag:yaml.org,2002:seq', result)

    def __init__(self, features_kwargs=(), always_bag=False):
        class Feature(self.Feature):
            __slots__ = ()
            system = self

        self.Feature = Feature

        self.mapping = collections.OrderedDict()
        for index, kwargs in enumerate(features_kwargs):
            f = self.create_feature(index, **kwargs)
            self.mapping[f.key] = f
        if not len(self.mapping) == len(features_kwargs):
            raise ValueError('%r no uniqueness.')

        self.specificities = sorted(set(f.specificity
            for f in itervalues(self.mapping)), reverse=True)

        self.categories = tools.uniqued(f.category
            for f in itervalues(self.mapping))

        class FeatureSet(self.FeatureSet):
            system = self

        class FeatureBag(self.FeatureBag):
            system = self

        self.FeatureSet = FeatureSet
        self.FeatureBag = FeatureBag

        FeatureMeta.system = FeatureSetMeta.system = self

        self.always_bag = bool(always_bag)
        if always_bag:
            # change the base of already referenced class
            FeatureSet.__bases__ = (FeatureBag,)
            FeatureSet.__name__ = 'FeatureBag'

    def __len__(self):
        return len(self.mapping)

    def __iter__(self):
        return itervalues(self.mapping)

    def __getitem__(self, index):
        return list(self.mapping.values())[index]

    _tdrop = ' ,;'
    _trans = (None, _tdrop) if PY2 else (str.maketrans('', '', _tdrop),)

    @staticmethod
    def create_value(value, _trans=_trans):
        if isinstance(value, int):
            return '%+d' % value
        return str(value).translate(*_trans)

    @staticmethod
    def get_key(value):
        return str(value).lower().lstrip('+')

    def create_feature(self, index, value, category=None, specificity=0, name=None):
        value = self.create_value(value)
        if not value:
            raise ValueError('%r empty value.' % self)

        name = str(name).title() if name else self.derive_name(value)

        class Feature(self.Feature):
            __slots__ = ()

        Feature.__name__ = '%sFeature' % name
        Feature.name = name
        Feature.index = int(index)
        Feature.key = self.get_key(value)
        Feature.value = value
        Feature.category = str(category).lower() if category else ''
        Feature.specificity = int(specificity)
        return Feature

    _derive_replaces = [
        [('+', 'plus'), ('-', 'minus')],
        [('1', 'first'), ('2', 'second'), ('3', 'third')],
        [('sg', 'singular'), ('du', 'dual'), ('pl', 'plural')],
    ]

    @classmethod
    def derive_name(cls, value):
        parts = []
        for srpl in cls._derive_replaces:
            for s, r in srpl:
                if value.startswith(s):
                    value = value[len(s):]
                    parts.append(r)
                    break
        parts.append(value)
        return ''.join(p.title() for p in parts)
