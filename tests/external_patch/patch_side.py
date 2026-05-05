def patchedM(self):
    return 'patched'


def foreignModuleLevel():
    return 'foreign_foo'


def foreignExtra(_self):
    return 'extra'


def foreignStatic():
    return 'static'


def foreignClsmethod(cls):
    return cls.__name__ + ':cls'


def foreignProp(self):
    return 'prop'
