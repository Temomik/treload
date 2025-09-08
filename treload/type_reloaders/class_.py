import types

from treload.utils import updateScope, processCallback
from treload.logger import logTrace, logError


def check(old, new, name):
    classType = getattr(types, 'ClassType', type)
    return (isinstance(new, (classType, type)) or
            getattr(new, '__metaclass__', 1) == getattr(new, '__class__', -1))


def update(old, new, name, namespace):
    """Update a class object."""

    isChangesFound = False
    olddict = old.__dict__
    newdict = new.__dict__

    oldnames = set(olddict)
    newnames = set(newdict)

    for name in newnames - oldnames:
        setattr(old, name, newdict[name])
        logTrace('Added:', name, 'to', old)
        isChangesFound = True

    # Note: not removing old things...
    for name in oldnames - newnames:
        logTrace('Removed:', name, 'from', old)
        delattr(old, name)
        isChangesFound = True

    for name in (oldnames & newnames) - set(['__dict__', '__doc__']):
        isChangesFound |= updateScope(olddict[name], newdict[name], name, old)

    oldBases = getattr(old, '__bases__', None)
    newBases = getattr(new, '__bases__', None)
    if str(oldBases) != str(newBases):
        logError('Changing the hierarchy of a class is not supported. %s may be inconsistent.' % (old,))

    isChangesFound |= processCallback(old, new)

    return isChangesFound
