from treload.utils import updateScope


def check(old, new, name):
    return isinstance(new, classmethod)


def update(old, new, name, namespace):
    """Update a classmethod update."""
    # While we can't modify the classmethod object itself (it has no
    # mutable attributes), we *can* extract the underlying function
    # (by calling __get__(), which returns a method object) and update
    # it in-place.  We don't have the class available to pass to
    # __get__() but any object except None will do.
    return updateScope(old.__get__(0), new.__get__(0), name, old)
