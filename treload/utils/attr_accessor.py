from treload.utils.utils import getAttr, setAttr


class attrAccessor(object):
    def __init__(self, namespace):
        object.__setattr__(self, 'namespace', namespace)

    def __getattr__(self, name):
        return getAttr(self.namespace, name)

    def __setattr__(self, name, value):
        return setAttr(self.namespace, name, value)
