CHANGE_FLAG = False
DELETED_CONSTANT = 'old'
MODULE_RENAMED_FROM = 'old'
GLOBAL_VALUE = False


class DeletedClass(object):
    VALUE = 'old'


def deletedFunction():
    return 'deleted-old'


def usesGlobalValue():
    return GLOBAL_VALUE


def funcAddDoc():
    return CHANGE_FLAG


def funcChangeDoc():
    """old doc"""
    return CHANGE_FLAG


def funcRemoveDoc():
    """old doc"""
    return CHANGE_FLAG
