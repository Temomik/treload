def foo():
    return 'foo_old'


def fooDeleted():
    return 'foo_old'


class Test(object):
    def foo(self):
        return 'foo_old'

    @staticmethod
    def fooStatic():
        return 'foo_old'

    @classmethod
    def fooCls(cls):
        return 'foo_old'
