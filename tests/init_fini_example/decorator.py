import tests

LINKS_COUNT = 0


def decorator(func):
    global LINKS_COUNT

    if not tests.IS_RELOADING:
        LINKS_COUNT += 1
        # here can be executed some code that create external link in pybind or etc.
        # this trick can help to avoid multiple creation of links

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
