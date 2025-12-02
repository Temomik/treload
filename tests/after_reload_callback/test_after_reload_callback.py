from old import mod
from treload import reload


def test_passing():
    assert not mod.CONSTANT
    assert not mod.FuncCallback.CONSTANT
    assert not mod.ClsCallback.CONSTANT
    assert not mod.StaticCallback.CONSTANT
    assert not mod.Proxy.Inner.CALLBACK

    assert reload(mod)

    assert mod.CONSTANT
    assert not mod.FuncCallback.CONSTANT  # bound methods not supported
    assert mod.ClsCallback.CONSTANT
    assert mod.StaticCallback.CONSTANT
    assert not mod.Proxy.Inner.CALLBACK  # TODO support callbacks in closures
