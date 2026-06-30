from old import mod
from treload import reload


def test_containerSizeMismatchSkipsReplacement():
    assert mod.FLAG == 'old'
    assert mod.LIST_VALUE == [1]
    assert mod.DICT_VALUE == {'a': 1}
    assert mod.SET_VALUE == set([1])
    assert mod.TUPLE_VALUE == (1,)
    assert mod.EMPTY_LIST_VALUE == []
    assert mod.EMPTY_DICT_VALUE == {}
    assert mod.EMPTY_SET_VALUE == set()
    assert mod.EMPTY_TUPLE_VALUE == ()

    assert reload(mod)

    assert mod.FLAG == 'new'
    assert mod.LIST_VALUE == [1]
    assert mod.DICT_VALUE == {'a': 1}
    assert mod.SET_VALUE == set([1])
    assert mod.TUPLE_VALUE == (1,)
    assert mod.EMPTY_LIST_VALUE == [1]
    assert mod.EMPTY_DICT_VALUE == {'a': 1}
    assert mod.EMPTY_SET_VALUE == set([1])
    assert mod.EMPTY_TUPLE_VALUE == (1,)
