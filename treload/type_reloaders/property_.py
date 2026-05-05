import types

from treload.logger import logTrace
from treload.utils.utils import codeObjectsEqual, updateScope

_ACCESSOR_NAMES = ('fget', 'fset', 'fdel')


def check(old, new, name):
    return isinstance(new, property)


def update(old, new, name, namespace):
    isChangesFound = False
    # ``property.__doc__`` is read-only on CPython 2, so any docstring change has to
    # go through a full rebuild; otherwise ``help()``/IDE tooltips stay stale.
    needsRebuild = old.__doc__ != new.__doc__

    for accessor in _ACCESSOR_NAMES:
        oldFunc = getattr(old, accessor, None)
        newFunc = getattr(new, accessor, None)

        if (oldFunc is None) != (newFunc is None):
            needsRebuild = True
            continue

        if oldFunc is None:
            continue

        if not (isinstance(oldFunc, types.FunctionType) and isinstance(newFunc, types.FunctionType)):
            needsRebuild = True
            continue

        if codeObjectsEqual(oldFunc.__code__, newFunc.__code__):
            continue

        # Delegate to the function reloader via updateScope so accessors get the
        # full treatment: __code__, __doc__, __defaults__, __dict__ and a
        # recursive walk over __closure__. namespace=None disables the fallback
        # ``setAttr(namespace, name, new)`` branch in function.update so we can
        # never accidentally replace the property itself with a bare function.
        if updateScope(oldFunc, newFunc, '%s/%s' % (name, accessor), None):
            logTrace('Updated property accessor:', name, '/', accessor)
            isChangesFound = True

    if needsRebuild:
        _rebuildProperty(old, new, name, namespace)
        return True

    return isChangesFound


def _rebuildProperty(old, new, name, namespace):
    liveGlobals = _liveGlobalsFor(old)
    resolved = []
    for accessor in _ACCESSOR_NAMES:
        oldFunc = getattr(old, accessor, None)
        newFunc = getattr(new, accessor, None)

        if newFunc is None:
            resolved.append(None)
            if oldFunc is not None:
                logTrace('Removed property accessor:', name, '/', accessor)
        elif oldFunc is not None:
            resolved.append(oldFunc)
        else:
            resolved.append(_rebindGlobals(newFunc, liveGlobals))
            logTrace('Added property accessor:', name, '/', accessor)

    setattr(
        namespace,
        name,
        property(resolved[0], resolved[1], resolved[2], getattr(new, '__doc__', None)),
    )


def _liveGlobalsFor(old):
    for accessor in _ACCESSOR_NAMES:
        existing = getattr(old, accessor, None)
        if isinstance(existing, types.FunctionType):
            return existing.__globals__
    return None


def _rebindGlobals(func, liveGlobals):
    """Return a copy of *func* whose ``__globals__`` is ``liveGlobals``.

    ``__globals__`` is read-only on a live function, so we materialise a new
    function object that shares the original code, defaults and closure.
    """
    if not isinstance(func, types.FunctionType) or liveGlobals is None or func.__globals__ is liveGlobals:
        return func

    rebound = types.FunctionType(
        func.__code__,
        liveGlobals,
        func.__name__,
        func.__defaults__,
        func.__closure__,
    )
    rebound.__dict__.update(func.__dict__)
    rebound.__doc__ = func.__doc__
    return rebound
