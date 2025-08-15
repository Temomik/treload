def getCodeObject(baseFunc, modName, paths):
    return baseFunc('new', paths)


def resolvePkgPaths(baseFunc, pkgName):
    return baseFunc(pkgName)
