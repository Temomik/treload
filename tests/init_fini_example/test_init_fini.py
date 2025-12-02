from old import decorator

from treload import reload


def test_passing():
    assert decorator.LINKS_COUNT == 0

    from old import mod
    assert not mod.func()
    assert decorator.LINKS_COUNT == 1

    assert reload(mod)
    assert mod.func()
    assert decorator.LINKS_COUNT == 1

    decorator.decorator(lambda: None)
    assert decorator.LINKS_COUNT == 2
