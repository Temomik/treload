MODULE_VAR = True


class TestCls(object):
    CLASS_VAR = True

    @staticmethod
    def staticMethod():
        return True

    @classmethod
    def classMethod(cls):
        return True

    def method(self):
        return True


def func():
    return True
