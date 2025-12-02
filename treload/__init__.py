from treload.infrastructure import apply
from treload.logger import logTrace
from treload.utils.utils import init, fini


def reload(mod):
    """Reload a module in place, updating classes, methods and functions.

    mod: a module object

    Returns a boolean indicating whether a change was done.
    """
    # pydevd_dont_trace.clear_trace_filter_cache()
    init()
    result = apply(mod)
    fini()

    logTrace('treload completed with state - ', result)

    return result
