def func():
    def closure1():
        def closure2():
            def closure3():
                return False

            return closure3()

        return closure2()

    return closure1()


class TestCls(object):
    def method(self):
        def closure():
            return False

        return closure()

    @staticmethod
    def staticMethod():
        def closure():
            return False

        return closure()

    @classmethod
    def classMethod(cls):
        def closure():
            return False

        return closure()
