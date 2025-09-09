import decorator

from treload import reload


def test_passing():
    assert decorator.LINKS_COUNT == 0

    from tests.init_fini_example import old
    assert not old.func()
    assert decorator.LINKS_COUNT == 1

    assert reload(old)
    assert old.func()
    assert decorator.LINKS_COUNT == 1

    decorator.decorator(lambda: None)
    assert decorator.LINKS_COUNT == 2
