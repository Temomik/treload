class Base(object):
    def getViewModel(self):
        return 'new'


class Child(Base):
    @property
    def viewModel(self):
        return super(Child, self).getViewModel()
