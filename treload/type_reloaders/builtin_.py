from treload.logger import logTrace


def check(old, new, name):
    if name.startswith('__') and name.endswith('__'):
        return False

    allowedRange = [dict, tuple, list, set, float, int, str, bool]

    for item in allowedRange:
        if type(new) == item:
            return True

    return False


def update(old, new, name):
    return
    # TODO fix that it's not working

    if namespace[name] == newValue:
        return
    namespace[name] = newValue
    logTrace('Updated builtin:', name, 'to', id(newValue))
