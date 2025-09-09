from tests.inheritance_override import old
from treload import reload


def test_passing():
    instance = old.Child()

    assert not instance.getBoolean()
    assert not instance.PROPERTY

    assert reload(old)

    assert instance.getBoolean()
    assert instance.PROPERTY

    # in case if instance created after reload, then base implementation is accessible.
    assert not super(old.Child, old.Child()).getBoolean()
