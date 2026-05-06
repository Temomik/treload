def marker(func):
    def wrapper():
        return 'old:' + func()

    return wrapper


def plainToDecorate():
    return 'plain-old'


@marker
def decoratedToChange():
    return 'inner-old'


@marker
def decoratedToRemove():
    return 'inner-old'
