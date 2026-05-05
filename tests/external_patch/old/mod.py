from external_patch.patch_side import (
    foreignClsmethod,
    foreignExtra,
    foreignModuleLevel,
    foreignProp,
    foreignStatic,
    patchedM,
)

VALUE = 'old'


class C(object):
    def m(self):
        return 'class_old'


C.m = patchedM
C.extra = foreignExtra
C.extraStatic = staticmethod(foreignStatic)
C.extraCls = classmethod(foreignClsmethod)
C.extraProp = property(foreignProp)


def foo():
    return 'foo_old'


foo = foreignModuleLevel
