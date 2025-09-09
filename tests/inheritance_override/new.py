from tests.inheritance_override.base import Base


class Child(Base):
    PROPERTY = True

    def getBoolean(self):
        # super(Child, self).getBoolean()
        # calling Base func will raise TypeError:
        return True
