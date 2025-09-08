from treload.logger import logTrace
from treload.utils import codeObjectsEqual


def check(old, new, name):
    return isinstance(new, property)


def update(old, new, name, namespace):
    setattr(namespace, name,
            property(getattr(new, 'fget', None),
                     getattr(new, 'fset', None),
                     getattr(new, 'fdel', None),
                     getattr(new, 'doc', None)))

    return True
