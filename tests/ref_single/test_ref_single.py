from tests.ref_single.old import mod
from tests.with_reload import batchReload


def foreignModuleLevel(*args, **kwargs):
    return 'foreign_foo'


_MOD_NAME = 'treload_tests_ref_single_mod'


def updateCachedRef_function():
    setattr(mod, '_treload_ref_foo', mod.foo)
    setattr(mod, '_treload_ref_fooDeleted', mod.fooDeleted)
    mod.foo = foreignModuleLevel
    mod.fooDeleted = foreignModuleLevel

    assert mod.foo is foreignModuleLevel
    assert mod.foo() == 'foreign_foo'

    assert mod._treload_ref_foo() == 'foo_old'

    yield

    assert mod.foo is foreignModuleLevel
    assert mod.foo() == 'foreign_foo'
    assert mod._treload_ref_foo() == 'foo_new'


def updateCachedRef_cls():
    Test = mod.Test
    cls = Test()

    setattr(Test, '_treload_ref_foo', Test.__dict__['foo'])
    setattr(Test, '_treload_ref_fooCls', Test.__dict__['fooCls'])
    setattr(Test, '_treload_ref_fooStatic', Test.__dict__['fooStatic'])

    Test.foo = foreignModuleLevel
    Test.fooCls = foreignModuleLevel
    Test.fooStatic = foreignModuleLevel

    assert cls.foo() == 'foreign_foo'
    assert Test().foo() == 'foreign_foo'
    assert Test().fooCls() == 'foreign_foo'
    assert Test().fooStatic() == 'foreign_foo'

    assert Test()._treload_ref_foo() == 'foo_old'
    assert Test._treload_ref_fooCls() == 'foo_old'
    assert Test._treload_ref_fooStatic() == 'foo_old'

    yield

    assert cls.foo() == 'foreign_foo'
    assert Test().foo() == 'foreign_foo'
    assert Test().fooCls() == 'foreign_foo'
    assert Test().fooStatic() == 'foreign_foo'

    assert Test()._treload_ref_foo() == 'foo_new'
    assert Test._treload_ref_fooCls() == 'foo_new'
    assert Test._treload_ref_fooStatic() == 'foo_new'


@batchReload(
    tests=(updateCachedRef_function, updateCachedRef_cls),
    modules=(mod,),
)
def test_batch():
    pass
