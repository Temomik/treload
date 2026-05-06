def marker(func):
    def wrapper():
        return 'new:' + func()

    return wrapper


@marker
def plainToDecorate():
    return 'plain-new'


@marker
def decoratedToChange():
    return 'inner-new'


def decoratedToRemove():
    return 'plain-new'
