class Holder(object):
    """new class doc"""

    CHANGED_CONSTANT = True
    RENAMED_TO = 'new'

    def methodAddDoc(self):
        """added method doc"""
        return True

    def methodChangeDoc(self):
        """new method doc"""
        return True

    def methodRemoveDoc(self):
        return True

    @property
    def addedProperty(self):
        return 'added-new'


class ClassDocAdd(object):
    """added class doc"""

    VALUE = True


class ClassDocChange(object):
    """new class doc"""

    VALUE = True


class ClassDocRemove(object):
    VALUE = True
