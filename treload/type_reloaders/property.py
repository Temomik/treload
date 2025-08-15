from treload.logger import logTrace
from treload.utils import codeObjectsEqual


def check(old, new, name):
    return isinstance(new, property)


def update(old, new, name):
    items = ['fget', 'fset', 'fdel']
    isChangesFound = False

    for item in items:
        oldItem = getattr(old, item, None)
        newItem = getattr(new, item, None)

        # TODO remove newItem check?
        if oldItem is None or newItem is None:
            continue

        if codeObjectsEqual(oldItem.__code__, newItem.__code__):
            continue

        isChangesFound = True
        oldItem.__code__ = newItem.__code__
        logTrace('Updated property[{}]:'.format(item), name, 'to', id(new))

    return isChangesFound
