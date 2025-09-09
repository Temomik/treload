import importlib
import os
import traceback
from functools import partial
from os import path
import sys

import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    import imp  # TODO generic method for different python versions

from treload.logger import logError, logTrace

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


# TODO add better msg?
# logError('Exception found when updating %s. Proceeding for other items.' % (name,))
@noExcept
def updateScope(old, new, name, namespace):
    """
    Update old, if possible in place, with new.
    If old is immutable, this simply returns new.
    """
    logTrace('Updating: ', old)
    isChangesFound = False

    if old is new:
        # Probably something imported
        return False

    if type(old) is not type(new):
        # Cop-out: if the type changed, give up
        logError('Type of: %s changed... Skipping.' % (old,))
        return isChangesFound

    from treload.type_reloaders import TYPE_RELOADER_ITEMS
    for reloader in TYPE_RELOADER_ITEMS:
        if not reloader.check(old, new, name):
            continue
        isChangesFound |= reloader.update(old, new, name, namespace)

    return isChangesFound


def Exec(exp, global_vars, local_vars=None):
    if local_vars is not None:
        exec (exp, global_vars, local_vars)
    else:
        exec (exp, global_vars)


def codeObjectsEqual(lhs, rhs):
    for d in dir(lhs):
        if d.startswith('_') or 'lineno' in d:
            continue
        if IS_PY38_OR_GREATER and d == 'replace':
            continue
        if getattr(lhs, d) != getattr(rhs, d):
            return False
    return True


def codeObjectsMonkeypatched(code0, code1):
    """
    If the code name changed, the old code probably be monkey patched,
    but monkey patched code object may not change the code name.
    """
    return getattr(code0, 'co_name') != getattr(code1, 'co_name')


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
