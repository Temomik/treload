def foo():
    return 'foo_new'


class Test(object):
    def foo(self):
        return 'foo_new'

    @staticmethod
    def fooStatic():
        return 'foo_new'

    @classmethod
    def fooCls(cls):
        return 'foo_new'
