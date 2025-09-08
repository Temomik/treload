MODULE_PROPERTY_BOOL = True
MODULE_PROPERTY_STR = '123'
MODULE_PROPERTY_LIST = [1, 2, 3]
MODULE_PROPERTY_INT = 123


class PropertyTest(object):
    CLASS_PROPERTY_BOOL = True
    CLASS_PROPERTY_STR = '123'
    CLASS_PROPERTY_LIST = [1, 2, 3]
    CLASS_PROPERTY_INT = 123

    def __init__(self):
        self._private = False
        self._getterOnly = False

    @property
    def private(self):
        return self._private

    @private.setter
    def private(self, value):
        self._private = value

    @property
    def getterOnly(self):
        return self._getterOnly

    @getterOnly.setter
    def getterOnly(self, value):
        self._getterOnly = True
