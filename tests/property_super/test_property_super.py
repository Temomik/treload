from old import mod
from treload import reload


def test_super_in_property_after_reload():
    instance = mod.Child()
    assert instance.viewModel == 'old'

    assert reload(mod)

    assert instance.viewModel == 'new'
