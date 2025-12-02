from old import mod
from treload import reload


def test_passing():
    instance = mod.Child()

    assert not instance.getBoolean()
    assert not instance.PROPERTY

    assert reload(mod)

    assert instance.getBoolean()
    assert instance.PROPERTY

    # in case if instance created after reload, then base implementation is accessible.
    assert not super(mod.Child, mod.Child()).getBoolean()
