def methodMarker(func):
    def wrapper(self):
        return 'old:' + func(self)

    return wrapper


class DecoratorTarget(object):
    @methodMarker
    def decoratedMethodToChange(self):
        return 'inner-old'


class UnsupportedTarget(object):
    def methodToDecorate(self):
        return 'plain-old'

    @methodMarker
    def decoratedMethodToRemove(self):
        return 'inner-old'

    def methodToStatic(self):
        return 'method-old'

    @staticmethod
    def staticToMethod():
        return 'static-old'

    def methodToClass(self):
        return 'method-old'
