import os

import tests

_OLD = os.path.sep + 'old'
_NEW = os.path.sep + 'new'

def getCodeObject(baseFunc, modName, paths):
    paths = [path.replace(_OLD, _NEW) for path in paths if paths]
    return baseFunc(modName, paths)


def resolvePkgPaths(baseFunc, pkgName):
    return baseFunc(pkgName)


def init(_):
    tests.IS_RELOADING = True


def fini(_):
    tests.IS_RELOADING = False
