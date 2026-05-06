from tests.module_delete_docstrings.old import mod
from treload import reload


def test_moduleLevelDeletionUnsupported_andFunctionDocstringsReload():
    assert mod.CHANGE_FLAG is False
    assert mod.DELETED_CONSTANT == 'old'
    assert mod.MODULE_RENAMED_FROM == 'old'
    assert not hasattr(mod, 'MODULE_RENAMED_TO')
    assert mod.usesGlobalValue() is False
    assert mod.deletedFunction() == 'deleted-old'
    assert mod.DeletedClass.VALUE == 'old'
    assert mod.funcAddDoc.__doc__ is None
    assert mod.funcChangeDoc.__doc__ == 'old doc'
    assert mod.funcRemoveDoc.__doc__ == 'old doc'

    assert reload(mod)

    assert mod.CHANGE_FLAG is True
    assert mod.MODULE_RENAMED_TO == 'new'
    assert mod.usesGlobalValue() is True
    assert mod.funcAddDoc()
    assert mod.funcChangeDoc()
    assert mod.funcRemoveDoc()
    assert mod.funcAddDoc.__doc__ == 'added doc'
    assert mod.funcChangeDoc.__doc__ == 'new doc'
    assert mod.funcRemoveDoc.__doc__ is None

    # Module-level deletion is intentionally unsupported by the current reloader.
    assert mod.DELETED_CONSTANT == 'old'
    assert mod.MODULE_RENAMED_FROM == 'old'
    assert mod.deletedFunction() == 'deleted-old'
    assert mod.DeletedClass.VALUE == 'old'
