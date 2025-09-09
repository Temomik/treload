import os

from treload.logger import logTrace
from treload.scope_data import g_scopeData
from treload.utils.utils import Exec, resolvePkgPaths, getCodeObject, noExcept, processCallback, updateScope


@noExcept
def apply(module):
    # TODO add callbacks
    isChangesFound = False

    modName = module.__name__  # Get the module name, e.g. 'foo.bar.whatever'
    pkgName = os.path.dirname(module.__file__)
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
    newNamespace["__name__"] = modns["__name__"]
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
        isChangesFound |= updateScope(modns[name], newNamespace[name], name, modns)

    isChangesFound |= processCallback(modns)

    g_scopeData.collect()

    return isChangesFound
