from old import mod
from treload import reload


def test_passing():
    assert not hasattr(mod, 'MODULE_VAR')
    assert not hasattr(mod, 'func')
    assert not hasattr(mod, 'TestCls')

    assert reload(mod)

    assert mod.MODULE_VAR, 'failed to add module variable'
    assert mod.func(), 'failed to add func'
    assert mod.TestCls.CLASS_VAR, 'failed to add class variable'
    assert mod.TestCls.staticMethod(), 'failed to add static method'
    assert mod.TestCls.classMethod(), 'failed to add class method'
    assert mod.TestCls().method(), 'failed to add class method'
