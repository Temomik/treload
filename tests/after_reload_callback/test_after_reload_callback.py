from tests.after_reload_callback import old
from treload import reload


def test_passing():
    assert not old.CONSTANT
    assert not old.FuncCallback.CONSTANT
    assert not old.ClsCallback.CONSTANT
    assert not old.StaticCallback.CONSTANT
    assert not old.Proxy.Inner.CALLBACK

    assert reload(old)

    assert old.CONSTANT
    assert not old.FuncCallback.CONSTANT  # bound methods not supported
    assert old.ClsCallback.CONSTANT
    assert old.StaticCallback.CONSTANT
    assert not old.Proxy.Inner.CALLBACK  # TODO support callbacks in closures
