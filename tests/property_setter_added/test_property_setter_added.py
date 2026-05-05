import pytest

from old import mod
from treload import reload


def test_runtime_added_setter_uses_super():
    instance = mod.Child()
    assert instance.viewModel == 'old'

    with pytest.raises(AttributeError):
        instance.viewModel = 1

    assert reload(mod)

    assert instance.viewModel == 'new'

    instance.viewModel = 42
    assert instance.stored == ('new-set', 42)
