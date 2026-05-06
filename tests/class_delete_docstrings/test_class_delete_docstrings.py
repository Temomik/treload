from tests.class_delete_docstrings.old import mod
from treload import reload


def test_classMembersDelete_andMethodDocstringsReload():
    instance = mod.Holder()
    assert mod.Holder.__doc__ == 'old class doc'
    assert mod.Holder.CHANGED_CONSTANT is False
    assert mod.Holder.DELETED_CONSTANT == 'old'
    assert mod.Holder.RENAMED_FROM == 'old'
    assert not hasattr(mod.Holder, 'RENAMED_TO')
    assert instance.deletedMethod() == 'deleted-old'
    assert instance.deletedProperty == 'deleted-old'
    assert not hasattr(mod.Holder, 'addedProperty')
    assert mod.Holder.methodAddDoc.__doc__ is None
    assert mod.Holder.methodChangeDoc.__doc__ == 'old method doc'
    assert mod.Holder.methodRemoveDoc.__doc__ == 'old method doc'
    assert mod.ClassDocAdd.__doc__ is None
    assert mod.ClassDocChange.__doc__ == 'old class doc'
    assert mod.ClassDocRemove.__doc__ == 'old class doc'

    assert reload(mod)

    assert mod.ClassDocAdd.VALUE is True
    assert mod.ClassDocChange.VALUE is True
    assert mod.ClassDocRemove.VALUE is True
    assert mod.Holder.CHANGED_CONSTANT is True
    assert not hasattr(mod.Holder, 'DELETED_CONSTANT')
    assert not hasattr(mod.Holder, 'RENAMED_FROM')
    assert mod.Holder.RENAMED_TO == 'new'
    assert not hasattr(mod.Holder, 'deletedMethod')
    assert not hasattr(mod.Holder, 'deletedProperty')
    assert instance.addedProperty == 'added-new'
    assert instance.methodAddDoc()
    assert instance.methodChangeDoc()
    assert instance.methodRemoveDoc()
    assert mod.Holder.methodAddDoc.__doc__ == 'added method doc'
    assert mod.Holder.methodChangeDoc.__doc__ == 'new method doc'
    assert mod.Holder.methodRemoveDoc.__doc__ is None

    # Existing class __doc__ is skipped by class.update().
    assert mod.Holder.__doc__ == 'old class doc'
    assert mod.ClassDocAdd.__doc__ is None
    assert mod.ClassDocChange.__doc__ == 'old class doc'
    assert mod.ClassDocRemove.__doc__ == 'old class doc'
