from old import mod
from treload import reload


def test_passing():
    assert not mod.overrideFunc()
    assert not mod.proxyFunc()
    assert not mod.noneFunc()
    assert not mod.treload_decorator_noneFunc()

    assert reload(mod)

    assert mod.proxyFunc()
    assert mod.overrideFunc()
    assert mod.newFunc()
    assert mod.noneFunc()
    assert mod.treload_decorator_noneFunc()
