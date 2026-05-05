class Base(object):
    def __init__(self):
        self.stored = None

    def getViewModel(self):
        return 'new'

    def setViewModel(self, value):
        self.stored = ('new-set', value)


class Child(Base):
    @property
    def viewModel(self):
        return super(Child, self).getViewModel()

    @viewModel.setter
    def viewModel(self, value):
        super(Child, self).setViewModel(value)
