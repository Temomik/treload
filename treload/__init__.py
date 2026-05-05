from treload.infrastructure import apply
from treload.logger import logTrace
from treload.utils.utils import init, fini


def reload(mod):
    """Reload a module in place, updating classes, methods and functions.

    mod: a module object

    Returns a boolean indicating whether a change was done.
    """
    init()
    result = apply(mod)
    fini()

    return result
