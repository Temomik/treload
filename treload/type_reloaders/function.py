import types

from treload.logger import logTrace, logError
from treload.utils import codeObjectsEqual, codeObjectsMonkeypatched, updateScope


def check(old, new, name):
    return isinstance(new, types.FunctionType)


def update(old, new, name, namespace):
    """Update a function object."""
    isChangesFound = False

    old.__doc__ = new.__doc__
    old.__dict__.update(new.__dict__)

    try:
        new.__code__  # pylint: disable=pointless-statement
        attrName = '__code__'
    except AttributeError:
        new.func_code  # pylint: disable=pointless-statement
        attrName = 'func_code'

    oldCode = getattr(old, attrName)
    newCode = getattr(new, attrName)

    if codeObjectsMonkeypatched(oldCode, newCode):
        logError('Code of: %s monkey patched... Skipping.' % (old,))
        return False

    if not codeObjectsEqual(oldCode, newCode):
        logTrace('Updated function code:', old)
        setattr(old, attrName, newCode)
        isChangesFound = True

    try:
        old.__defaults__ = new.__defaults__
    except AttributeError:
        old.func_defaults = new.func_defaults

    # Update func_closure:
    # 1, skip if function closure count mismatch,
    # 2, only do update by the same function closure sequence.

    try:
        new.__closure__
        closureAttrName = '__closure__'
    except AttributeError:
        new.func_closure
        closureAttrName = 'func_closure'

    old_closure = getattr(old, closureAttrName) or []
    new_closure = getattr(new, closureAttrName) or []

    if len(old_closure) != len(new_closure):
        logError('Closure count of: %s changed... Skipping.' % (old,))
        return isChangesFound

    for old_cell, new_cell in zip(old_closure, new_closure):
        isChangesFound |= updateScope(old_cell.cell_contents, new_cell.cell_contents, name, old_cell)

    return isChangesFound
