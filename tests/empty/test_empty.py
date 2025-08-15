from tests.empty import old
from treload import reload


def test_passing():
    assert not reload(old)
