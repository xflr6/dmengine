# types.py - customized collection classes

from itertools import starmap

from ._compat import map, with_metaclass

from . import meta

__all__ = ['List', 'FlowList', 'Instances', 'StarInstances']


@meta.serializable
class List(with_metaclass(meta.EmptySlotsMeta, list)):
    """YAML serializable list with type-preserving copy and getslice."""

    @staticmethod
    def _multi_representer(dumper, self):
        return dumper.represent_sequence('tag:yaml.org,2002:seq', self)

    def __init__(self, items=()):
        super(List, self).__init__(items)

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__,
                           super(List, self).__repr__())

    def __getslice__(self, start, end):
        return self.__class__(super(List, self).__getslice__(start, end))

    def copy(self):
        return self.__class__(item.copy() for item in self)


@meta.serializable
class FlowList(List):
    """List with flow-style YAML representation."""

    @staticmethod
    def _multi_representer(dumper, self):
        return dumper.represent_sequence('tag:yaml.org,2002:seq', self,
                                         flow_style=True)


class Instances(List):
    """List of instances created applying **kwargs to factory function."""

    new_item = None

    def __init__(self, items_kwargs=()):
        new_item = self.new_item
        items = (new_item(**kwargs) for kwargs in items_kwargs)
        super(Instances, self).__init__(items)

    def __repr__(self):
        return '[%s]' % ',\n '.join(map(repr, self))


class StarInstances(List):
    """List of instances created applying *args to factory function."""

    new_item = None

    def __init__(self, items_args=()):
        items = starmap(self.new_item, items_args)
        super(StarInstances, self).__init__(items)

    def __repr__(self):
        return '[%s]' % ',\n '.join(map(repr, self))
