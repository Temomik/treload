CHANGE_FLAG = True
MODULE_RENAMED_TO = 'new'
GLOBAL_VALUE = True


def funcAddDoc():
    """added doc"""
    return CHANGE_FLAG


def funcChangeDoc():
    """new doc"""
    return CHANGE_FLAG


def funcRemoveDoc():
    return CHANGE_FLAG


def usesGlobalValue():
    return GLOBAL_VALUE
