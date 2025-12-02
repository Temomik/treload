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
    return False


@override(False)
def overrideFunc():
    return True
