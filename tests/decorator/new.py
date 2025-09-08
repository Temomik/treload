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


@proxy
def proxyFunc():
    return True


@override(True)
def overrideFunc():
    return False


@override(True)
def newFunc():
    return False
