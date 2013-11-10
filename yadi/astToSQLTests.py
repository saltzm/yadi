'''
r = RelationInQuery('', {Variable():,}, {Constant():,},[],False)
q = Query([],[],[Variable(),]) 

class RelationInQuery:

    def __init__(self, name='', variables={},constants = {},wildcards = [], is_negated = False):
        self.name = name # The name of the relation
        self.variables = variables # {Variable -> Position}
        self.constants = constants # {Constant -> Position}
        self.negated = False # Is it negated
        self.wildcards = wildcards # [position]  


class Query:
    def __init__(self, relations = [], constraints = [], head_variables = [] ):
        self.head_variables = head_variables
        self.relations = relations# [RelationInQuery].
        self.constraints = constraints # Explicit constraints of the form Element COMP Element type.
                                       # [(Element_1, Element_2, Comparison_operator)]
'''

# Q(X,Y):- S(X) Not Safe

r = RelationInQuery('S', {Variable('X'):0}, {},[],False)
q = Query([r],[],[Variable('X'), Variable('Y')]) 
bla = QueryToAlchemyStatement(q)
print 'Test 1'
print 'Correct: False'
print bla.check_is_it_safe()
print '-------------------'
print ''

# Q(X):- S(X) Safe

r = RelationInQuery('S', {Variable('X'):0}, {},[],False)
q = Query([r],[],[Variable('X')]) 
bla = QueryToAlchemyStatement(q)
print 'Test 2'
print 'Correct: True'
print bla.check_is_it_safe()
print '-------------------'
print ''

# Q(X):- S(X), !T(U) Not safe

s = RelationInQuery('S', {Variable('X'):0}, {},[],False)
t = RelationInQuery('T', {Variable('U'):0}, {},[],True)
q = Query([s,t],[],[Variable('X')]) 
bla = QueryToAlchemyStatement(q)
print 'Test 3'
print 'Correct: False'
print bla.check_is_it_safe()
print '-------------------'
print ''

# Q(X):- S(X,U), !T(U) Not safe

s = RelationInQuery('S', {Variable('X'):0,Variable('U'):1}, {},[],False)
t = RelationInQuery('T', {Variable('U'):0}, {},[],True)
q = Query([s,t],[],[Variable('X')]) 
bla = QueryToAlchemyStatement(q)
print 'Test 4'
print 'Correct: True'
print bla.check_is_it_safe()
print '-------------------'
print ''

# Q(X):- S(X), !T(U), U = 2 Safe

s = RelationInQuery('S', {Variable('X'):0,Variable('U'):1}, {},[],False)
t = RelationInQuery('T', {Variable('U'):0}, {},[],True)
q = Query([s,t],[(Variable('U'), Constant('2'), '==')],[Variable('X')]) 
bla = QueryToAlchemyStatement(q)
print 'Test 5'
print 'Correct: True'
print bla.check_is_it_safe()
print '-------------------'
print ''

# Q(X):- S(X), !T(U), U = 2 Safe

s = RelationInQuery('S', {Variable('X'):0,Variable('U'):1}, {},[],False)
t = RelationInQuery('T', {Variable('U'):0}, {},[],True)
q = Query([s,t],[(Variable('U'), Constant('2'), '<')],[Variable('X')]) 
bla = QueryToAlchemyStatement(q)
print 'Test 6'
print 'Correct: False'
print bla.check_is_it_safe()
print '-------------------'
print ''

