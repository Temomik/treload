# A comment added above shifts every function/method down.
# The bodies below are intentionally byte-identical to old/mod.py;
# only co_firstlineno / co_lnotab should differ.




def func():
    return 42


class TestCls(object):
    def method(self):
        return 42

    @staticmethod
    def staticMethod():
        return 42

    @classmethod
    def classMethod(cls):
        return 42
