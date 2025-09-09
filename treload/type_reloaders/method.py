import types

from treload.utils.utils import updateScope


def check(old, new, name):
    return isinstance(new, types.MethodType)


def update(old, new, name, namespace):
    """Update a method object."""
    # TODO What if im_func is not a function?
    if hasattr(old, 'im_func') and hasattr(new, 'im_func'):
        return updateScope(old.im_func, new.im_func, name, old)

    if hasattr(old, '__func__') and hasattr(new, '__func__'):
        return updateScope(old.__func__, new.__func__, name, old)

    return False
