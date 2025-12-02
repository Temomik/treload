from old import mod
from treload import reload


def test_passing():
    assert not mod.overrideFunc()
    assert not mod.proxyFunc()

    assert reload(mod)

    assert mod.proxyFunc()
    assert not mod.overrideFunc()  # TODO already decorated function can reloaded partialy
    assert mod.newFunc()  # function decorated after reload is supported
