from treload.logger import logError


class ScopeData(object):

    def __init__(self):
        super(ScopeData, self).__init__()

        self.endReloadQuery = list()

    def collect(self):
        for item in self.endReloadQuery:
            try:
                item()
            except Exception as e:
                logError(str(e), str(item.args))

        self.__reset()

    def __reset(self):
        self.endReloadQuery = list()


g_scopeData = ScopeData()
