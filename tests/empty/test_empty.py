from old import mod
from treload import reload


def test_passing():
    assert not reload(mod)
