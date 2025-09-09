from treload.utils.utils import updateScope


def check(old, new, name):
    return isinstance(new, staticmethod)


def update(old, new, name, namespace):
    """Update a staticmethod update."""
    # While we can't modify the staticmethod object itself (it has no
    # mutable attributes), we *can* extract the underlying function
    # (by calling __get__(), which returns it) and update it in-place.
    # We don't have the class available to pass to __get__() but any
    # object except None will do.
    return updateScope(old.__get__(0), new.__get__(0), name, old)
