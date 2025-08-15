class ScopeData(object):

    def __init__(self):
        super(ScopeData, self).__init__()

        self.endReloadQuery = list()

    def collect(self):
        for item in self.endReloadQuery:
            item()

        self.__reset()

    def __reset(self):
        self.endReloadQuery = list()


g_scopeData = ScopeData()
