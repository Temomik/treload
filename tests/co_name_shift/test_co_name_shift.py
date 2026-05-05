"""Reload must replace __code__ when co_name differs (same attribute name, different def name)."""
from old import mod
from treload import reload


def test_func_updates_when_inner_co_name_differs():
    assert mod.func.__code__.co_name == 'func'
    assert not mod.func()

    assert reload(mod)

    assert mod.func.__code__.co_name == '_impl'
    assert mod.func()
