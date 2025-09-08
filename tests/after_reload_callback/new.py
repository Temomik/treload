CONSTANT = False


def __treload__(new, old):
    new['CONSTANT'] = True


class FuncCallback(object):
    CONSTANT = False

    def __treload__(self, new, old):
        self.CONSTANT = True


class ClsCallback(object):
    CONSTANT = False

    @classmethod
    def __treload__(cls, new, old):
        cls.CONSTANT = True


class StaticCallback(object):
    CONSTANT = False

    @staticmethod
    def __treload__(new, old):
        setattr(new, 'CONSTANT', True)
