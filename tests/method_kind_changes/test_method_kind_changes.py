from tests.method_kind_changes.old import mod
from treload import reload


def test_classMethodDecoratorAndKindChanges():
    decoratorInstance = mod.DecoratorTarget()
    unsupportedInstance = mod.UnsupportedTarget()
    assert decoratorInstance.decoratedMethodToChange() == 'old:inner-old'
    assert unsupportedInstance.methodToDecorate() == 'plain-old'
    assert unsupportedInstance.decoratedMethodToRemove() == 'old:inner-old'
    assert unsupportedInstance.methodToStatic() == 'method-old'
    assert mod.UnsupportedTarget.staticToMethod() == 'static-old'
    assert unsupportedInstance.staticToMethod() == 'static-old'
    assert unsupportedInstance.methodToClass() == 'method-old'

    assert reload(mod)

    assert decoratorInstance.decoratedMethodToChange() == 'new:inner-new'

    # Adding/removing a closure-based decorator changes function freevars.
    assert unsupportedInstance.methodToDecorate() == 'plain-old'
    assert unsupportedInstance.decoratedMethodToRemove() == 'old:inner-old'

    # Switching between function, staticmethod and classmethod changes the
    # descriptor type, so updateScope() skips the existing attribute.
    assert unsupportedInstance.methodToStatic() == 'method-old'
    assert mod.UnsupportedTarget.staticToMethod() == 'static-old'
    assert unsupportedInstance.staticToMethod() == 'static-old'
    assert unsupportedInstance.methodToClass() == 'method-old'
