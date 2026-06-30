from treload.logger import logTrace
from treload.utils.utils import setAttr


def check(old, new, name):
    if name.startswith('__') and name.endswith('__'):
        return False

    allowedRange = [dict, tuple, list, set, float, int, str, bool]

    for item in allowedRange:
        if type(new) == item:
            return True

    return False


def _isContainer(value):
    return type(value) in (dict, tuple, list, set)


def update(old, new, name, namespace):
    if _isContainer(old) and _isContainer(new) and len(old) > 0 and len(new) == 0:
        logTrace('Skipped builtin container update to preserve non-empty cache:', name)
        return False

    result = True
    try:
        setAttr(namespace, name, new)
        logTrace('Updated builtin:', name, 'to', new)
    except:
        result = False

    return result
