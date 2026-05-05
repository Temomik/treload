"""Aliased classes (``Alias = TheClass``) must be processed only once per reload.
"""
from old import mod
from treload import reload


def test_aliased_class_processed_once_per_reload():
    assert mod.TheClass is mod.Alias, 'precondition: alias points to the same class'
    assert mod.TheClass.VALUE == 'old'
    assert mod.RELOAD_INVOCATIONS[0] == 0

    assert reload(mod)

    assert mod.TheClass.VALUE == 'new'
    assert mod.TheClass is mod.Alias, 'alias must keep pointing at the same class'
    assert mod.RELOAD_INVOCATIONS[0] == 1, (
        'class.update must run once per reload regardless of how many module-level '
        'aliases reference the class; got %d invocations' % (mod.RELOAD_INVOCATIONS[0],)
    )
