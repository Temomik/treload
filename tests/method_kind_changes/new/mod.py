def methodMarker(func):
    def wrapper(self):
        return 'new:' + func(self)

    return wrapper


class DecoratorTarget(object):
    @methodMarker
    def decoratedMethodToChange(self):
        return 'inner-new'


class UnsupportedTarget(object):
    @methodMarker
    def methodToDecorate(self):
        return 'plain-new'

    def decoratedMethodToRemove(self):
        return 'plain-new'

    @staticmethod
    def methodToStatic():
        return 'static-new'

    def staticToMethod(self):
        return 'method-new'

    @classmethod
    def methodToClass(cls):
        return 'class-new'
