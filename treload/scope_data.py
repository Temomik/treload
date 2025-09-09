from treload.logger import logError
from treload.utils.attr_accessor import attrAccessor


class ScopeData(object):

    def __init__(self):
        super(ScopeData, self).__init__()

        self.endReloadQuery = list()

    def collect(self):
        for callback, namespace in self.endReloadQuery:
            try:
                callback(attrAccessor(namespace))
            except Exception as e:
                logError(str(e), str(callback))

        self.__reset()

    def __reset(self):
        self.endReloadQuery = list()


g_scopeData = ScopeData()
