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

import copy

# SAFETY TESTS
# Q(X,Y):- S(X) Not Safe

r = RelationInQuery('S', {Variable('X'):[0]}, {},[],False)
q = Query([r],[],[Variable('X'), Variable('Y')]) 
bla = QueryToAlchemyStatement(q)
print 'Test 1'
print 'Correct: False'
print bla.check_is_it_safe()
print '-------------------'
print ''

# Q(X):- S(X) Safe

r = RelationInQuery('S', {Variable('X'):[0]}, {},[],False)
q = Query([r],[],[Variable('X')]) 
bla = QueryToAlchemyStatement(q)
print 'Test 2'
print 'Correct: True'
print bla.check_is_it_safe()
print '-------------------'
print ''

# Q(X):- S(X), !T(U) Not safe

s = RelationInQuery('S', {Variable('X'):[0]}, {},[],False)
t = RelationInQuery('T', {Variable('U'):[0]}, {},[],True)
q = Query([s,t],[],[Variable('X')]) 
bla = QueryToAlchemyStatement(q)
print 'Test 3'
print 'Correct: False'
print bla.check_is_it_safe()
print '-------------------'
print ''

# Q(X):- S(X,U), !T(U) Not safe

s = RelationInQuery('S', {Variable('X'):[0],Variable('U'):[1]}, {},[],False)
t = RelationInQuery('T', {Variable('U'):[0]}, {},[],True)
q = Query([s,t],[],[Variable('X')]) 
bla = QueryToAlchemyStatement(q)
print 'Test 4'
print 'Correct: True'
print bla.check_is_it_safe()
print '-------------------'
print ''

# Q(X):- S(X), !T(U), U = 2 Safe

s = RelationInQuery('S', {Variable('X'):[0],Variable('U'):[1]}, {},[],False)
t = RelationInQuery('T', {Variable('U'):[0]}, {},[],True)
q = Query([s,t],[[Variable('U'), Constant('2'), '==']],[Variable('X')]) 
bla = QueryToAlchemyStatement(q)
print 'Test 5'
print 'Correct: True'
print bla.check_is_it_safe()
print '-------------------'
print ''

# Q(X):- S(X), !T(U), U < 2 Safe

s = RelationInQuery('S', {Variable('X'):[0],Variable('U'):[1]}, {},[],False)
t = RelationInQuery('T', {Variable('U'):[0]}, {},[],True)
q = Query([s,t],[[Variable('U'), Constant('2'), '<']],[Variable('X')]) 
bla = QueryToAlchemyStatement(q)
print 'Test 6'
print 'Correct: False'
print bla.check_is_it_safe()
print '-------------------'
print ''

# EQUALITY CONSTRAINTS REDUCTION TESTS:

# Q(X):- S(X), X = 2
r = RelationInQuery('S', {Variable('X'):[0]}, {},[],False)
q = Query([r],[[Variable('X'), Constant('2'), '=']],[Variable('X')]) 
bla = QueryToAlchemyStatement(q)
print 'Test 1'
print 'Original: '
print q
print ''
print bla.reduce_equality_constraints(q)
print '-------------------'
print ''

# Q(X):- S(X, Y), Y = 2
r = RelationInQuery('S', {Variable('X'):[0], Variable('Y'):[1]}, {},[],False)
q = Query([r],[[Variable('Y'), Constant('2'), '=']],[Variable('X')]) 
bla = QueryToAlchemyStatement(q)
print 'Test 2'
print 'Original: '
print q
print ''
print bla.reduce_equality_constraints(q)
print '-------------------'
print ''

# Q(X):- S(X, Y, Z), Y = 2, Z = Y
r = RelationInQuery('S', {Variable('X'):[0], Variable('Y'):[1], Variable('Z'):[2]}, {},[],False)
q = Query([r],[[Variable('Y'), Constant('2'), '='], [Variable('Z'), Variable('Y'), '=']],[Variable('X')]) 
bla = QueryToAlchemyStatement(q)
print 'Test 3'
print 'Original: '
print q
print ''
print bla.reduce_equality_constraints(q)
print '-------------------'
print ''

#  Q(X) := not S(Y),  X = 2, X = Y,
r = RelationInQuery('S', {Variable('Y'):[0]}, {},[],True)
q = Query([r],[[Variable('X'), Constant('2'), '='], [Variable('X'), Variable('Y'), '=']],[Variable('X')]) 
bla = QueryToAlchemyStatement(q)
print 'Test 4'
print 'Original: '
print q
print ''
print bla.reduce_equality_constraints(q)
print '-------------------'
print ''

#  Q(X) := not S(Y), X = Y, X = 2
r = RelationInQuery('S', {Variable('Y'):[0]}, {},[],True)
q = Query([r],[[Variable('X'), Variable('Y'), '='],[Variable('X'), Constant('2'), '=']],[Variable('X')]) 
bla = QueryToAlchemyStatement(q)
print 'Test 5'
print 'Original: '
print q
print ''
print bla.reduce_equality_constraints(q)
print '-------------------'
print ''
