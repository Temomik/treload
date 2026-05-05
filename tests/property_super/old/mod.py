class Base(object):
    def getViewModel(self):
        return 'old'


class Child(Base):
    @property
    def viewModel(self):
        return super(Child, self).getViewModel()
