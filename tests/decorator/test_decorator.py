from tests.decorator import old
from treload import reload


def test_passing():
    assert not old.overrideFunc()
    assert not old.proxyFunc()

    assert reload(old)

    assert old.proxyFunc()
    assert not old.overrideFunc()  # TODO already decorated function can reloaded partialy
    assert old.newFunc()  # function decorated after reload is supported
