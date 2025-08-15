def func():
    def closure1():
        def closure2():
            def closure3():
                return True

            return closure3()

        return closure2()

    return closure1()


class TestCls(object):
    def method(self):
        def closure():
            return True

        return closure()

    @staticmethod
    def staticMethod():
        def closure():
            return True

        return closure()

    @classmethod
    def classMethod(cls):
        def closure():
            return True

        return closure()
