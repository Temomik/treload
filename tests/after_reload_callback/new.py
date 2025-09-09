CONSTANT = False


def __treload__(namespace):
    # namespace is current module
    namespace.CONSTANT = True


class FuncCallback(object):
    CONSTANT = False

    def __treload__(self, namespace):
        # will not work
        pass


class ClsCallback(object):
    CONSTANT = False

    @classmethod
    def __treload__(cls, namespace):
        # namespace is StaticCallback
        namespace.CONSTANT = True


class StaticCallback(object):
    CONSTANT = False

    @staticmethod
    def __treload__(namespace):
        # namespace is StaticCallback
        namespace.CONSTANT = True


class Proxy(object):
    class Inner(object):
        CALLBACK = False

        @staticmethod
        def __treload__(namespace):
            # namespace is Inner
            # will not work
            namespace.CONSTANT = True
