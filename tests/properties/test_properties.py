from tests.properties import old
from treload import reload

# properties imported using (from *** import ***) have to be handled manually via __treload__ callback
from tests.properties.old import MODULE_PROPERTY_BOOL


def test_passing():
    instance = old.PropertyTest()
    instance.private = True

    assert not MODULE_PROPERTY_BOOL
    assert not old.MODULE_PROPERTY_BOOL
    assert not instance.private
    assert not instance.getterOnly
    assert not old.PropertyTest.CLASS_PROPERTY_BOOL
    assert not old.PropertyTest.CLASS_PROPERTY_STR
    assert not old.PropertyTest.CLASS_PROPERTY_LIST
    assert not old.PropertyTest.CLASS_PROPERTY_INT
    assert not instance.CLASS_PROPERTY_BOOL
    assert not instance.CLASS_PROPERTY_STR
    assert not instance.CLASS_PROPERTY_LIST
    assert not instance.CLASS_PROPERTY_INT

    assert reload(old)

    instance.private = True
    instance.getterOnly = True

    assert not MODULE_PROPERTY_BOOL
    assert old.MODULE_PROPERTY_BOOL
    assert instance.private
    assert instance.getterOnly
    assert old.PropertyTest.CLASS_PROPERTY_BOOL
    assert old.PropertyTest.CLASS_PROPERTY_STR
    assert old.PropertyTest.CLASS_PROPERTY_LIST
    assert old.PropertyTest.CLASS_PROPERTY_INT
    assert instance.CLASS_PROPERTY_BOOL
    assert instance.CLASS_PROPERTY_STR
    assert instance.CLASS_PROPERTY_LIST
    assert instance.CLASS_PROPERTY_INT
