from treload.logger import logError
from treload.utils.attr_accessor import attrAccessor


class ScopeData(object):

    def __init__(self):
        super(ScopeData, self).__init__()

        self.endReloadQuery = list()

        # Reentrancy guard for updateScope: tracks (id(old), id(new)) pairs currently
        # being updated on the call stack. Prevents infinite recursion when an object
        # transitively references itself through closures or globals (e.g. a function
        # wrapped by a decorator that captures the original function in its closure,
        # such as updateScope itself, which is decorated with @noExcept).
        self.updateScopeInProgressIds = set()

    def collect(self):
        for callback, namespace in self.endReloadQuery:
            try:
                callback(attrAccessor(namespace))
            except Exception as e:
                logError(str(e), str(callback))

        self.reset()

    def reset(self):
        self.endReloadQuery = list()
        self.updateScopeInProgressIds = set()


g_scopeData = ScopeData()
