class Element:
    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.__dict__ == other.__dict__)
    def is_variable(self):
        return isinstance(self,Variable)
    def is_constant(self):
        return isinstance(self,Constant)
    def is_wildcard(self):
        return isinstance(self,Wildcard)

class Variable(Element):
    def __init__(self,name = ''):
        self.name = name
    def __hash__(self):
        return hash(self.name)
    def __repr__(self):
        return self.name

class Constant(Element):
    def __init__(self,value = ''):
        self.value = value
    def __hash__(self):
        return hash(self.value)
    def __repr__(self):
        return self.value

class Wildcard(Element):
    def __hash__(self):
        return hash('_')
    def __repr__(self):
        return '_'

