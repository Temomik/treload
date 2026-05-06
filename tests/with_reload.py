from functools import wraps

from treload import reload


def batchReload(tests, modules):
    """Two-phase batch decorator.

    The decorated function is replaced with a body that:
      1. instantiates a generator from each test in ``tests``,
      2. advances every generator to its ``yield`` (pre-yield asserts run for ALL tests),
      3. calls ``reload(m)`` once per module in ``modules``,
      4. advances every generator past ``yield`` (post-yield asserts run for ALL tests).
    """

    def decorator(testFunc):
        @wraps(testFunc)
        def wrapper(*args, **kwargs):
            gens = [test() for test in tests]
            for gen in gens:
                next(gen)

            for module in modules:
                assert reload(module)

            for gen in gens:
                try:
                    next(gen)
                except StopIteration:
                    pass

        return wrapper

    return decorator
