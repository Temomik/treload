def proxy(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def override(result):
    def proxy(func):
        def wrapper(*args, **kwargs):
            return result

        return wrapper

    return proxy


def noneProxy(func):
    func.__globals__["treload_decorator_" + func.__name__] = func

    def wrapper():
        return None

    return wrapper


@proxy
def proxyFunc():
    return False


@override(False)
def overrideFunc():
    return True


@noneProxy
def noneFunc():
    return False
