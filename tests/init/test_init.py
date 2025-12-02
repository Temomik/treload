from treload import reload

import old
def test_passing():
    assert not old.getBool()
    assert not old.VARIABLE

    assert reload(old)

    assert old.getBool()
    assert old.VARIABLE
