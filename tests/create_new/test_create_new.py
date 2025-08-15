from tests.create_new import old
from treload import reload


def test_passing():
    assert not hasattr(old, 'MODULE_VAR')
    assert not hasattr(old, 'func')
    assert not hasattr(old, 'TestCls')

    assert reload(old)

    assert old.MODULE_VAR, 'failed to add module variable'
    assert old.func(), 'failed to add func'
    assert old.TestCls.CLASS_VAR, 'failed to add class variable'
    assert old.TestCls.staticMethod(), 'failed to add static method'
    assert old.TestCls.classMethod(), 'failed to add class method'
    assert old.TestCls().method(), 'failed to add class method'
