"""Meta-programming tools."""

import collections

import yaml

__all__ = ['serializable', 'EmptySlotsMeta', 'FactoryMeta']


def serializes(data_type):
    """Register decorated function as YAML representer for type."""
    def decorator(func):
        yaml.add_representer(data_type, func)
        return func
    return decorator


@serializes(collections.OrderedDict)
def odict_representer(dumper, self):
    """Serialize OrderedDict items in their order."""
    return dumper.represent_mapping('tag:yaml.org,2002:map', self.items())


def serializable(cls):
    """Register representer method of decorated class with YAML."""
    if hasattr(cls, '_representer'):
        yaml.add_representer(cls, cls._representer)
    elif hasattr(cls, '_multi_representer'):
        yaml.add_multi_representer(cls, cls._multi_representer)
    else:
        raise RuntimeError
    return cls


class EmptySlotsMeta(type):
    """Set empty __slots__ on all derived classes."""

    def __new__(cls, name, bases, dct):
        dct['__slots__'] = ()
        return super().__new__(cls, name, bases, dct)


def FactoryMeta(key_attr, mapping_type=dict):  # noqa: N802
    """Return a metaclass that registers and retrieves subclasses by nonempty key_attr class attribute."""
    class FactoryMeta(type):

        def __init__(self, name, bases, dct):  # noqa: N804
            if not hasattr(self, '_FactoryMeta__factory'):
                self.__factory = self
                self.__mapping = mapping_type()
            else:
                key = dct.get(key_attr)
                if key:
                    self.__mapping[key] = self
            super().__init__(name, bases, dct)

        def __call__(self, *args, **kwargs):  # noqa: N804
            if self is self.__factory:
                try:
                    key, args = args[0], args[1:]
                except IndexError:
                    try:
                        key = kwargs.pop(key_attr)
                    except KeyError:
                        raise TypeError(f'{self!r} is a factory, must specify'
                                        f' {key_attr} keyword of the class'
                                        ' to instantiate')

                try:
                    cls = self.__mapping[key]
                except (KeyError, TypeError):
                    raise TypeError(f'{key!r} is not a registered'
                                    f' {key_attr} keyword for {self!r}')

                assert issubclass(cls, self)
                self = cls
            return super().__call__(*args, **kwargs)

        @property
        def subclasses(self):  # noqa: N804
            if self is self.__factory:
                return self.__mapping
            raise NotImplementedError

    return FactoryMeta
