from old import mod
from treload import reload


def test_passing():
    oldInstance = mod.TestCls()

    assert not mod.func()
    assert not oldInstance.method()
    assert not oldInstance.staticMethod()
    assert not oldInstance.classMethod()

    assert reload(mod)

    assert mod.func(), 'failed to reload module closure'
    # assert mod.TestCls().method(), 'failed to reload method closure'
    assert oldInstance.staticMethod(), 'failed to reload static method closure'
    assert oldInstance.classMethod(), 'failed to reload class method closure'

    assert mod.TestCls().staticMethod(), 'failed to reload static method closure'
    assert mod.TestCls().classMethod(), 'failed to reload class method closure'
