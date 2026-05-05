RELOAD_INVOCATIONS = [0]


class TheClass(object):
    VALUE = 'new'

    @staticmethod
    def __treload__(_):
        RELOAD_INVOCATIONS[0] += 1


Alias = TheClass
