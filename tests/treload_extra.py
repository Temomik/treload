import tests


def getCodeObject(baseFunc, modName, paths):
    return baseFunc('new', paths)


def resolvePkgPaths(baseFunc, pkgName):
    return baseFunc(pkgName)


def init(_):
    tests.IS_RELOADING = True


def fini(_):
    tests.IS_RELOADING = False
