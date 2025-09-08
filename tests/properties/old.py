MODULE_PROPERTY_BOOL = False
MODULE_PROPERTY_STR = ''
MODULE_PROPERTY_LIST = []
MODULE_PROPERTY_INT = 0


class PropertyTest(object):
    CLASS_PROPERTY_BOOL = False
    CLASS_PROPERTY_STR = ''
    CLASS_PROPERTY_LIST = []
    CLASS_PROPERTY_INT = 0

    @property
    def private(self):
        return False

    @private.setter
    def private(self, value):
        pass

    @property
    def getterOnly(self):
        return False
