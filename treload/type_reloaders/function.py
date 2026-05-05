import sys
import types

from treload.logger import logTrace, logError
from treload.utils.utils import codeObjectsEqual, setAttr, updateScope

if sys.version_info[0] < 3:
    import __builtin__ as _builtins  # pylint: disable=import-error

    _closureScalarTypes = (
        bool, int, _builtins.long, float, complex, str, _builtins.unicode, type(None),
    )
else:
    _closureScalarTypes = (bool, int, float, complex, str, bytes, type(None))


def _isClosureScalar(value):
    """True for immutable closure captures that cannot use updateScope in place."""
    return isinstance(value, _closureScalarTypes)


def _tryAssignCellContents(cell, value):
    """Write into a closure cell when the interpreter allows it (e.g. CPython 3.7+)."""
    try:
        cell.cell_contents = value
        return True
    except (AttributeError, ValueError, TypeError):
        return False


def _canReplaceBoundFunction(namespace):
    """True if we may swap the live object via setAttr (module or class), not a closure cell."""
    if namespace is None:
        return False
    return type(namespace).__name__ != 'cell'


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
        oldContents = old_cell.cell_contents
        newContents = new_cell.cell_contents
        if updateScope(oldContents, newContents, name, old_cell):
            isChangesFound = True
        elif (
                type(oldContents) is type(newContents)
                and oldContents != newContents
                and _isClosureScalar(oldContents)
                and _isClosureScalar(newContents)
        ):
            if _tryAssignCellContents(old_cell, newContents):
                isChangesFound = True
            elif _canReplaceBoundFunction(namespace):
                setAttr(namespace, name, new)
                return True

    return isChangesFound
