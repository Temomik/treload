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
        return True

    return wrapper


@proxy
def proxyFunc():
    return True


@override(True)
def overrideFunc():
    return False


@override(True)
def newFunc():
    return False


@noneProxy
def noneFunc():
    return True
