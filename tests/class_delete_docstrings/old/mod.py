class Holder(object):
    """old class doc"""

    CHANGED_CONSTANT = False
    DELETED_CONSTANT = 'old'
    RENAMED_FROM = 'old'

    def methodAddDoc(self):
        return False

    def methodChangeDoc(self):
        """old method doc"""
        return False

    def methodRemoveDoc(self):
        """old method doc"""
        return False

    def deletedMethod(self):
        return 'deleted-old'

    @property
    def deletedProperty(self):
        return 'deleted-old'


class ClassDocAdd(object):
    VALUE = False


class ClassDocChange(object):
    """old class doc"""

    VALUE = False


class ClassDocRemove(object):
    """old class doc"""

    VALUE = False
