from old import mod
from treload import reload


def test_property_docstring_refreshed_after_reload():
    instance = mod.Holder()
    assert instance.value == 1
    assert mod.Holder.value.__doc__ == 'old doc'
    assert mod.Holder.value.fget.__doc__ == 'old doc'

    assert reload(mod)

    assert instance.value == 2
    assert mod.Holder.value.fget.__doc__ == 'new doc'
    assert mod.Holder.value.__doc__ == 'new doc'
