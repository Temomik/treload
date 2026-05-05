import importlib
import os
import traceback
from functools import partial
from os import path
import sys

import warnings

from treload.utils.constants import TRELOAD_REFS_ATTR, SKIP_START_WITH_NAMES, SKIP_UPDATE_NAMES

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    import imp  # TODO generic method for different python versions

from treload.logger import logError, logDebug

try:
    IS_PY38_OR_GREATER = sys.version_info >= (3, 8)
except AttributeError:
    # Not all versions have sys.version_info
    IS_PY38_OR_GREATER = False

# global storage for after reload callbacks
g_callbacks = list()


def noExcept(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:  # pylint: disable=bare-except
            logError(str(e))
            traceback.print_exc()

    return wrapper


def noExceptCallback(exceptionCallback):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:  # pylint: disable=bare-except
                logError(str(e))
                traceback.print_exc()
                exceptionCallback(e)

        return wrapper

    return decorator


def extraOverride(func):
    @noExcept
    def wrapper(*args, **kwargs):
        resultFunc = func
        try:
            treload = importlib.import_module('treload_extra')
            resultFunc = getattr(treload, func.__name__)
            resultFunc = partial(resultFunc, func)
        except (AttributeError, ImportError):
            pass

        return resultFunc(*args, **kwargs)

    return wrapper


def processCallback(namespace):
    from treload.scope_data import g_scopeData

    callback = getAttr(namespace, '__treload__')
    if not callable(callback):
        return False

    g_scopeData.endReloadQuery.append((callback, namespace))
    return True


def getAttr(namespace, name, default=None):
    if isinstance(namespace, dict):
        return namespace.get(name, default)
    return getattr(namespace, name, default)


def setAttr(namespace, name, value):
    if isinstance(namespace, dict):
        namespace[name] = value
        return True
    setattr(namespace, name, value)


@noExcept
def updateScope(old, new, name, namespace):
    """
    Update old, if possible in place, with new.
    If old is immutable, this simply returns new.
    """
    from treload.scope_data import g_scopeData

    for prefix in SKIP_START_WITH_NAMES:
        if name.startswith(prefix):
            logDebug('Internal object... Skipping.', name)
            return False

    if name in SKIP_UPDATE_NAMES:
        logDebug('Internal object... Skipping.', name)
        return False

    if old is new:
        # Probably something imported
        logDebug('The same object ... Skipping.', new)
        return False

    if type(old) is not type(new):
        # Cop-out: if the type changed, give up
        logDebug('Type of: %s changed... Skipping.', new)
        return False

    key = (id(old), id(new))
    if key in g_scopeData.updateScopeInProgressIds:
        logDebug('Recursive update detected... Skipping.', name)
        return False

    g_scopeData.updateScopeInProgressIds.add(key)
    try:
        logDebug('Updating: ', name, old)
        from treload.type_reloaders import TYPE_RELOADER_ITEMS
        for reloader in TYPE_RELOADER_ITEMS:
            if not reloader.check(old, new, name):
                continue

            return reloader.update(old, new, name, namespace)

        return False
    finally:
        g_scopeData.updateScopeInProgressIds.discard(key)


def Exec(exp, global_vars, local_vars=None):
    if local_vars is not None:
        exec (exp, global_vars, local_vars)
    else:
        exec (exp, global_vars)


def codeObjectsEqual(lhs, rhs):
    for d in dir(lhs):
        if d.startswith('_'):
            continue
        if IS_PY38_OR_GREATER and d == 'replace':
            continue
        if getattr(lhs, d) != getattr(rhs, d):
            return False
    return True


@extraOverride
def resolvePkgPaths(pkgName):
    return [path.normpath(pkgName), ]


@extraOverride
def getCodeObject(modname, paths):
    modname = modname.rsplit(".", 1)[-1]  # extract name [foo.bar.name -> name]

    for path in paths:
        filePath = os.path.join(path, modname) + '.py'
        if not os.path.exists(filePath):
            continue

        with open(filePath, 'r') as stream:
            source = stream.read()
            return compile(source, filePath, "exec")

    return None


@extraOverride
def init():
    pass


@extraOverride
def fini():
    pass


def clearTraceFilterCache():
    try:
        from _pydevd_bundle.pydevd_dont_trace import clear_trace_filter_cache
        clear_trace_filter_cache()
    except ImportError:
        pass


def updateInternalRefs(modns, newNamespace):
    """Update in-place objects registered by the module under a stable key.

    Contract:
        _treload_refs_ : Dict[str, List[object]]

    Old and new modules must keep the same key->list shape; otherwise we skip updates for that key.
    """
    isChangesFound = False

    oldRefs = modns.get(TRELOAD_REFS_ATTR)
    newRefs = newNamespace.get(TRELOAD_REFS_ATTR)

    if isinstance(newRefs, dict) and not isinstance(oldRefs, dict):
        # First load of refs in an already-imported module (or refs added later): just publish them.
        modns[TRELOAD_REFS_ATTR] = newRefs
        return True

    if not (isinstance(oldRefs, dict) and isinstance(newRefs, dict)):
        return False

    # Add new keys (note: not deleting existing keys).
    for key in set(newRefs) - set(oldRefs):
        oldRefs[key] = newRefs[key]
        isChangesFound = True

    # Update existing keys in-place.
    for key in set(oldRefs) & set(newRefs):
        oldList = oldRefs.get(key)
        newList = newRefs.get(key)
        if not isinstance(oldList, (list, tuple)) or not isinstance(newList, (list, tuple)):
            logError("%s['%s'] is not list/tuple. Skipping." % (TRELOAD_REFS_ATTR, key))
            continue

        if len(oldList) != len(newList):
            logError(
                "%s['%s'] length changed (%d -> %d). Skipping." % (TRELOAD_REFS_ATTR, key, len(oldList), len(newList)))
            continue

        for i in range(len(oldList)):
            # Use namespace=None so reloaders won't try to replace by setAttr on a wrong container.
            isChangesFound |= updateScope(oldList[i], newList[i], "%s[%d]" % (key, i), None)

    return isChangesFound
