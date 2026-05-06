from tests.decorator_plain.old import mod
from treload import reload


def test_plainDecoratorChangeWorks_addRemoveUnsupported():
    assert mod.plainToDecorate() == 'plain-old'
    assert mod.decoratedToChange() == 'old:inner-old'
    assert mod.decoratedToRemove() == 'old:inner-old'

    assert reload(mod)

    assert mod.decoratedToChange() == 'new:inner-new'

    # Adding/removing a closure-based decorator changes function freevars and is
    # currently skipped by function.update().
    assert mod.plainToDecorate() == 'plain-old'
    assert mod.decoratedToRemove() == 'old:inner-old'
