from treload.logger import logTrace


def check(old, new, name):
    if name.startswith('__') and name.endswith('__'):
        return False

    allowedRange = [dict, tuple, list, set, float, int, str, bool]

    for item in allowedRange:
        if type(new) == item:
            return True

    return False


def update(old, new, name, namespace):
    result = True
    try:
        namespace[name] = new
        logTrace('Updated builtin:', name, 'to', new)
    except:
        result = False
    try:
        setattr(namespace, name, new)
        logTrace('Updated builtin:', name, 'to', new)
    except:
        result = False

    return result
