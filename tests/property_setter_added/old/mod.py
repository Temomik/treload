class Base(object):
    def __init__(self):
        self.stored = None

    def getViewModel(self):
        return 'old'

    def setViewModel(self, value):
        self.stored = ('old-set', value)


class Child(Base):
    @property
    def viewModel(self):
        return super(Child, self).getViewModel()
