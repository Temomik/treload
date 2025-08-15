from tests.closures import old
from treload import reload


def test_passing():
    oldInstance = old.TestCls()

    assert not old.func()
    assert not oldInstance.method()
    assert not oldInstance.staticMethod()
    assert not oldInstance.classMethod()

    assert reload(old)

    assert old.func(), 'failed to reload module closure'
    # assert old.TestCls().method(), 'failed to reload method closure'
    assert oldInstance.staticMethod(), 'failed to reload static method closure'
    assert oldInstance.classMethod(), 'failed to reload class method closure'

    assert old.TestCls().staticMethod(), 'failed to reload static method closure'
    assert old.TestCls().classMethod(), 'failed to reload class method closure'
