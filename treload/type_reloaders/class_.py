import types

from treload.utils.utils import updateScope, processCallback
from treload.logger import logTrace, logError

SKIP_CLASS_ATTRIBUTE_NAMES = {
    '__dict__',
    '__doc__',
    '__firstlineno__',
    '__module__',
    '__qualname__',
    '__slots__',
    '__static_attributes__',
    '__weakref__',
}


def _functionGlobalsName(func):
    globs = getattr(func, 'func_globals', None) or getattr(func, '__globals__', None)
    return globs.get('__name__') if isinstance(globs, dict) else None


def _unwrapMethod(value):
    if not isinstance(value, types.MethodType):
        return None
    inner = getattr(value, 'im_func', None) or getattr(value, '__func__', None)
    return inner if isinstance(inner, types.FunctionType) else None


def _unwrapDescriptor(value):
    """Return the underlying function for ``staticmethod``/``classmethod`` or None."""
    if not isinstance(value, (staticmethod, classmethod)):
        return None
    try:
        inner = value.__get__(0)
    except (TypeError, AttributeError):
        return None
    if isinstance(inner, types.FunctionType):
        return inner
    return _unwrapMethod(inner)


def _iterUnderlyingFunctions(value):
    """Yield ``FunctionType`` instances reachable from a class attribute value."""
    if isinstance(value, types.FunctionType):
        yield value
        return

    fromMethod = _unwrapMethod(value)
    if fromMethod is not None:
        yield fromMethod
        return

    fromDescriptor = _unwrapDescriptor(value)
    if fromDescriptor is not None:
        yield fromDescriptor
        return

    if isinstance(value, property):
        for accessor in (value.fget, value.fset, value.fdel):
            if isinstance(accessor, types.FunctionType):
                yield accessor


def _isForeignPatch(value, expectedModuleName):
    """True if *value* is a function-like attribute whose source lives in another module.

    A monkey-patched attribute keeps the patcher's ``func_globals['__name__']`` even after
    being attached to a class from another module, so it does not match the class module
    under reload and must not be deleted.
    """
    for func in _iterUnderlyingFunctions(value):
        if _functionGlobalsName(func) != expectedModuleName:
            return True
    return False


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

    for name in (newnames - oldnames) - SKIP_CLASS_ATTRIBUTE_NAMES:
        setattr(old, name, newdict[name])
        logTrace('Added:', name, 'to', old)
        isChangesFound = True

    # Note: not removing old things...
    classModuleName = getattr(old, '__module__', None)

    for name in oldnames - newnames:
        if name in SKIP_CLASS_ATTRIBUTE_NAMES:
            continue
        if classModuleName and _isForeignPatch(olddict[name], classModuleName):
            logTrace('Skipping remove of foreign patch:', name, 'from', old)
            continue
        logTrace('Removed:', name, 'from', old)
        delattr(old, name)
        isChangesFound = True

    for name in (oldnames & newnames) - SKIP_CLASS_ATTRIBUTE_NAMES:
        isChangesFound |= updateScope(olddict[name], newdict[name], name, old)

    oldBases = getattr(old, '__bases__', None)
    newBases = getattr(new, '__bases__', None)
    if str(oldBases) != str(newBases):
        logError('Changing the hierarchy of a class is not supported. %s may be inconsistent.' % (old,))

    isChangesFound |= processCallback(old)

    return isChangesFound
