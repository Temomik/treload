import os

from treload.logger import logTrace, logError
from treload.scope_data import g_scopeData
from treload.utils.constants import MODULE_METADATA_KEYS
from treload.utils.utils import (Exec, resolvePkgPaths, getCodeObject, processCallback, updateScope, noExceptCallback,
                                 clearTraceFilterCache, updateInternalRefSingle, updateInternalRefsDict)


def onExceptionOccur(_):
    logError('failed to apply. exception occur. resetting all states...')
    g_scopeData.reset()
    clearTraceFilterCache()


@noExceptCallback(onExceptionOccur)
def apply(module):
    isChangesFound = False
    g_scopeData.reset()

    pkgName, fileName = os.path.split(module.__file__)
    modName, _ = os.path.splitext(fileName)
    modns = module.__dict__  # Get the module namespace (dict) early; this is part of the type check

    paths = resolvePkgPaths(pkgName)
    code = getCodeObject(modName, paths)

    # Execute the code.  We copy the module dict to a temporary; then
    # clear the module dict; then execute the new code in the module
    # dict; then swap things back and around.  This trick (due to
    # Glyph Lefkowitz) ensures that the (readonly) __globals__
    # attribute of methods and functions is set to the correct dict
    # object.
    newNamespace = modns.copy()
    newNamespace.clear()
    # Keep loader metadata so exec() still behaves as this package: __path__ drives submodule lookup;
    # __package__ / __loader__ / __spec__ keep import semantics aligned with the loaded module.
    for _k in MODULE_METADATA_KEYS:
        if _k in modns:
            newNamespace[_k] = modns[_k]

    Exec(code, newNamespace)
    # Now we get to the hard part
    oldnames = set(modns)
    newnames = set(newNamespace)

    # Create new tokens (note: not deleting existing)
    for name in newnames - oldnames:
        logTrace('Added:', name, 'to namespace')
        # self.foundChange = True
        modns[name] = newNamespace[name]
        isChangesFound = True

    # Update in-place what we can
    for name in oldnames & newnames:
        isChangesFound |= bool(updateScope(modns[name], newNamespace[name], name, modns))

    isChangesFound |= bool(updateInternalRefSingle(oldnames - newnames, modns, newNamespace))
    isChangesFound |= bool(updateInternalRefsDict(modns, newNamespace))
    isChangesFound |= bool(processCallback(modns))

    g_scopeData.collect()
    clearTraceFilterCache()

    return isChangesFound
