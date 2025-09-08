from tests.after_reload_callback import old
from treload import reload


def test_passing():
    assert not old.CONSTANT
    assert not old.FuncCallback.CONSTANT
    assert not old.ClsCallback.CONSTANT
    assert not old.StaticCallback.CONSTANT

    assert reload(old)

    assert old.CONSTANT
    assert not old.FuncCallback.CONSTANT
    assert old.ClsCallback.CONSTANT
    assert old.StaticCallback.CONSTANT
