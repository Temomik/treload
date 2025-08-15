from treload.infrastructure import apply


def reload(mod):
    """Reload a module in place, updating classes, methods and functions.

    mod: a module object

    Returns a boolean indicating whether a change was done.
    """
    # pydevd_dont_trace.clear_trace_filter_cache()
    return apply(mod)
