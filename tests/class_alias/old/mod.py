RELOAD_INVOCATIONS = [0]


class TheClass(object):
    VALUE = 'old'

    @staticmethod
    def __treload__(_):
        RELOAD_INVOCATIONS[0] += 1


Alias = TheClass
