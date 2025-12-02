from old.pkg1.pkg2.pkg3 import mod
from treload import reload


def test_passing():
    assert not mod.getBool()
    assert not mod.VARIABLE

    assert reload(mod)

    assert mod.getBool()
    assert mod.VARIABLE
