from old import mod
from external_patch import patch_side
from treload import reload


def _impl(funcOrMethod):
    return getattr(funcOrMethod, 'im_func', funcOrMethod)


def test_reload_preservesForeignPatches_and_skipsDeletingForeignOnlyAttributes():
    assert _impl(mod.C.m) is patch_side.patchedM
    assert mod.C().m() == 'patched'

    assert mod.foo is patch_side.foreignModuleLevel
    assert mod.foo() == 'foreign_foo'
    assert mod.VALUE == 'old'

    assert _impl(mod.C.extra) is patch_side.foreignExtra
    assert mod.C.extraStatic() == 'static'
    assert mod.C.extraCls() == 'C:cls'
    assert mod.C().extraProp == 'prop'

    assert reload(mod)

    assert _impl(mod.C.m) is patch_side.patchedM
    assert mod.C().m() == 'patched'

    assert mod.foo is patch_side.foreignModuleLevel
    assert mod.foo() == 'foreign_foo'

    assert mod.VALUE == 'new'

    assert hasattr(mod.C, 'extra')
    assert _impl(mod.C.extra) is patch_side.foreignExtra
    assert mod.C().extra() == 'extra'

    assert hasattr(mod.C, 'extraStatic')
    assert mod.C.extraStatic() == 'static'

    assert hasattr(mod.C, 'extraCls')
    assert mod.C.extraCls() == 'C:cls'

    assert hasattr(mod.C, 'extraProp')
    assert mod.C().extraProp == 'prop'
