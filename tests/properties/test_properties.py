from old import mod
from treload import reload

# properties imported using (from *** import ***) have to be handled manually via __treload__ callback
from old.mod import MODULE_PROPERTY_BOOL


def test_passing():
    instance = mod.PropertyTest()
    instance.private = True

    assert not MODULE_PROPERTY_BOOL
    assert not mod.MODULE_PROPERTY_BOOL
    assert not instance.private
    assert not instance.getterOnly
    assert not mod.PropertyTest.CLASS_PROPERTY_BOOL
    assert not mod.PropertyTest.CLASS_PROPERTY_STR
    assert not mod.PropertyTest.CLASS_PROPERTY_LIST
    assert not mod.PropertyTest.CLASS_PROPERTY_INT
    assert not instance.CLASS_PROPERTY_BOOL
    assert not instance.CLASS_PROPERTY_STR
    assert not instance.CLASS_PROPERTY_LIST
    assert not instance.CLASS_PROPERTY_INT

    assert reload(mod)

    instance.private = True
    instance.getterOnly = True

    assert not MODULE_PROPERTY_BOOL
    assert mod.MODULE_PROPERTY_BOOL
    assert instance.private
    assert instance.getterOnly
    assert mod.PropertyTest.CLASS_PROPERTY_BOOL
    assert mod.PropertyTest.CLASS_PROPERTY_STR
    assert mod.PropertyTest.CLASS_PROPERTY_LIST
    assert mod.PropertyTest.CLASS_PROPERTY_INT
    assert instance.CLASS_PROPERTY_BOOL
    assert instance.CLASS_PROPERTY_STR
    assert instance.CLASS_PROPERTY_LIST
    assert instance.CLASS_PROPERTY_INT
