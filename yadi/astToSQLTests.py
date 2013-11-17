#from .dataStructures.query import *
#from .dataStructures.relation import *
#from .dataStructures.element import *
#from .dataStructures.constraint import *
#from .queryExecutor.queryExecutor import *
#
#'''
#r = RelationInQuery('', {Variable():,}, {Constant():,},[],False)
#q = ConjunctiveQuery([],[],[Variable(),])
#
#class RelationInQuery:
#
#    def __init__(self, name='', variables={},constants = {},wildcards = [], is_negated = False):
#        self.name = name # The name of the relation
#        self.variables = variables # {Variable -> Position}
#        self.constants = constants # {Constant -> Position}
#        self.negated = False # Is it negated
#        self.wildcards = wildcards # [position]
#
#
#class Query:
#    def __init__(self, relations = [], constraints = [], head_variables = [] ):
#        self.head_variables = head_variables
#        self.relations = relations# [RelationInQuery].
#        self.constraints = constraints # Explicit constraints of the form Element COMP Element type.
#                                       # [(Element_1, Element_2, Comparison_operator)]
#                                       '''
#
#
#import copy
#
#
#
## SAFETY TESTS
## Q(X,Y):- S(X) Not Safe
#
#r = RelationInQuery('S', {Variable('X'):[0]}, {},[],False)
#q = ConjunctiveQuery([r],[],RelationInQuery('Q',{Variable('X'):[0],Variable('Y'):[1]}))
#bla = QueryToAlchemyStatement(q)
#print ('Test 1')
#print ('Correct: False')
#try:
#    print (bla.check_is_it_safe())
#except Exception as e:
#    print (e)
#
#print ('-------------------')
#print ('')
#
## Q(X):- S(X) Safe
#
#r = RelationInQuery('S', {Variable('X'):[0]}, {},[],False)
#q = ConjunctiveQuery([r],[],RelationInQuery('Q',{Variable('X'):[0]}))
#bla = QueryToAlchemyStatement(q)
#print ('Test 2')
#print ('Correct: True')
#try:
#    print bla.check_is_it_safe()
#except Exception as e:
#    print e
#print ('-------------------')
#print ('')
#
## Q(X):- S(X), !T(U) Not safe
#
#s = RelationInQuery('S', {Variable('X'):[0]}, {},[],False)
#t = RelationInQuery('T', {Variable('U'):[0]}, {},[],True)
#q = ConjunctiveQuery([s,t],[],RelationInQuery('Q',{Variable('X'):[0]}))
#bla = QueryToAlchemyStatement(q)
#print ('Test 3')
#print ('Correct: False')
#try:
#    print (bla.check_is_it_safe())
#except Exception as e:
#    print (e)
#print ('-------------------')
#print ('')
#
## Q(X):- S(X,U), !T(U) Safe
#
#s = RelationInQuery('S', {Variable('X'):[0],Variable('U'):[1]}, {},[],False)
#t = RelationInQuery('T', {Variable('U'):[0]}, {},[],True)
#q = ConjunctiveQuery([s,t],[],RelationInQuery('Q',{Variable('X'):[0]}))
#bla = QueryToAlchemyStatement(q)
#print 'Test 4'
#print 'Correct: True'
#try:
#    print bla.check_is_it_safe()
#except Exception as e:
#    print e
#print '-------------------'
#print ''
#
## Q(X):- S(X), !T(U), U = 2 Safe
#
#s = RelationInQuery('S', {Variable('X'):[0],Variable('U'):[1]}, {},[],False)
#t = RelationInQuery('T', {Variable('U'):[0]}, {},[],True)
#q = ConjunctiveQuery([s,t],[Constraint(Variable('U'), Constant('2'), '==')],RelationInQuery('Q',{Variable('X'):[0]}))
#bla = QueryToAlchemyStatement(q)
#print 'Test 5'
#print 'Correct: True'
#try:
#    print bla.check_is_it_safe()
#except Exception as e:
#    print e
#print '-------------------'
#print ''
#
## Q(X):- S(X), !T(U), U < 2 Not safe
#
#s = RelationInQuery('S', {Variable('X'):[0]}, {},[],False)
#t = RelationInQuery('T', {Variable('U'):[0]}, {},[],True)
#q = ConjunctiveQuery([s,t],[Constraint(Constant('2'),Variable('U'), '<')],RelationInQuery('Q',{Variable('X'):[0]}))
#bla = QueryToAlchemyStatement(q)
#print 'Test 6'
#print 'Correct: False'
#try:
#    print bla.check_is_it_safe()
#except Exception as e:
#    print e
#print '-------------------'
#print ''
#
## Q(X):- S(X), !T(U), U=X Safe
#
#s = RelationInQuery('S', {Variable('X'):[0]}, {},[],False)
#t = RelationInQuery('T', {Variable('U'):[0]}, {},[],True)
#q = ConjunctiveQuery([s,t],[Constraint(Variable('U'), Variable('X'), '=')],RelationInQuery('Q',{Variable('X'):[0]}))
#bla = QueryToAlchemyStatement(q)
#print 'Test 7'
#print 'Correct: True'
#try:
#    bla.query= bla.preProcessQuery(bla.query)
#    print bla.check_is_it_safe()
#except Exception as e:
#    print e
#
#print '-------------------'
#print ''
#
## Q(X):- S(X), !T(U), U=X Safe
#
#s = RelationInQuery('S', {Variable('X'):[0]}, {},[],False)
#t = RelationInQuery('T', {Variable('U'):[0]}, {},[],True)
#q = ConjunctiveQuery([s,t],[Constraint(Variable('U'), Variable('X'), '=')],RelationInQuery('Q',{Variable('X'):[0]}))
#bla = QueryToAlchemyStatement(q)
#print 'Test 8'
#print 'Correct: True'
#try:
#    bla.query= bla.preProcessQuery(bla.query)
#    print bla.check_is_it_safe()
#except Exception as e:
#    print e
#
#print '-------------------'
#print ''
#
## Q(X):- S(X), Y<3 Not safe
#
#s = RelationInQuery('S', {Variable('X'):[0]}, {},[],False)
#
#q = ConjunctiveQuery([s],[Constraint(Variable('Y'), Constant('3'), '<')],RelationInQuery('Q',{Variable('X'):[0]}))
#bla = QueryToAlchemyStatement(q)
#print 'Test 9'
#print 'Correct: False'
#try:
#    bla.query= bla.preProcessQuery(bla.query)
#    print bla.check_is_it_safe()
#except NotSafeException as e:
#    print e
#
#print '-------------------'
#print ''
#
## Q(X):- S(X,Y), Y<3 Safe
#
#s = RelationInQuery('S', {Variable('X'):[0],Variable('Y'):[1]}, {},[],False)
#
#q = ConjunctiveQuery([s],[Constraint(Variable('Y'), Constant('3'), '<')],RelationInQuery('Q',{Variable('X'):[0]}))
#bla = QueryToAlchemyStatement(q)
#print 'Test 10'
#print 'Correct: True'
#try:
#    bla.query= bla.preProcessQuery(bla.query)
#    print bla.check_is_it_safe()
#except Exception as e:
#    print e
#
#print '-------------------'
#print ''
#
## Q(X):- S(X), !T(Y), X=Y
#
#s = RelationInQuery('S', {Variable('X'):[0]}, {},[],False)
#t = RelationInQuery('T', {Variable('Y'):[1]}, {},[],True)
#
#q = ConjunctiveQuery([s,t],[Constraint(Variable('X'), Variable('Y'), '=')],RelationInQuery('Q',{Variable('X'):[0]}))
#
#bla = QueryToAlchemyStatement(q)
#print 'Test 11'
#print 'Correct: True'
#try:
#    bla.query= bla.preProcessQuery(bla.query)
#    print bla.check_is_it_safe()
#except Exception as e:
#    print e
#
#print '-------------------'
#print ''
#
## Q(X,Z):- S(X,Y), !T(A,Z), Z = Y
#
#s = RelationInQuery('S', {Variable('X'):[0],Variable('Y'):[1]}, {},[],False)
#t = RelationInQuery('T', {Variable('A'):[0],Variable('Z'):[1]}, {},[],True)
#
#q = ConjunctiveQuery([s,t],[Constraint(Variable('Y'), Variable('Z'), '=')],RelationInQuery('Q',{Variable('X'):[0],Variable('Z'):[1]}))
#
#bla = QueryToAlchemyStatement(q)
#print 'Test 12'
#print 'Correct: False'
#try:
#    bla.query= bla.preProcessQuery(bla.query)
#    print bla.check_is_it_safe()
#except Exception as e:
#    print e
#
#print '-------------------'
#print ''
#
#
## EQUALITY CONSTRAINTS REDUCTION TESTS:
#
## Q(X):- S(X), X = 2
#r = RelationInQuery('S', {Variable('X'):[0]}, {},[],False)
#q = ConjunctiveQuery([r],[Constraint(Variable('X'), Constant('2'), '=')],RelationInQuery('S',{Variable('X'):[0]}))
#bla = QueryToAlchemyStatement(q)
#print 'Test 1'
#print 'Original: '
#print q
#print ''
#print bla.reduce_equality_constraints(q)
#print '-------------------'
#print ''
#
## Q(X):- S(X, Y), Y = 2
#r = RelationInQuery('S', {Variable('X'):[0], Variable('Y'):[1]}, {},[],False)
#q = ConjunctiveQuery([r],[Constraint(Variable('Y'), Constant('2'), '=')],RelationInQuery('S',{Variable('X'):[0]}))
#bla = QueryToAlchemyStatement(q)
#print 'Test 2'
#print 'Original: '
#print q
#print ''
#print bla.reduce_equality_constraints(q)
#print '-------------------'
#print ''
#
## Q(X):- S(X, Y, Z), Y = 2, Z = Y
#r = RelationInQuery('S', {Variable('X'):[0], Variable('Y'):[1], Variable('Z'):[2]}, {},[],False)
#q = ConjunctiveQuery([r],[Constraint(Variable('Y'), Constant('2'), '='), Constraint(Variable('Z'), Variable('Y'), '=')],RelationInQuery('S',{Variable('X'):[0]}))
#bla = QueryToAlchemyStatement(q)
#print 'Test 3'
#print 'Original: '
#print q
#print ''
#print bla.reduce_equality_constraints(q)
#print '-------------------'
#print ''
#
##  Q(X) := not S(Y),  X = 2, X = Y,
#r = RelationInQuery('S', {Variable('Y'):[0]}, {},[],True)
#q = ConjunctiveQuery([r],[Constraint(Variable('X'), Constant('2'), '='), Constraint(Variable('X'), Variable('Y'), '=')],RelationInQuery('S',{Variable('X'):[0]}))
#bla = QueryToAlchemyStatement(q)
#print 'Test 4'
#print 'Original: '
#print q
#print ''
#print bla.reduce_equality_constraints(q)
#print '-------------------'
#print ''
#
##  Q(X) := not S(Y), X = Y, X = 2
#r = RelationInQuery('S', {Variable('Y'):[0]}, {},[],True)
#q = ConjunctiveQuery([r],[Constraint(Variable('X'), Variable('Y'), '='),Constraint(Variable('X'), Constant('2'), '=')],RelationInQuery('S',{Variable('X'):[0]}))
#bla = QueryToAlchemyStatement(q)
#print 'Test 5'
#print 'Original: '
#print q
#print ''
#print bla.reduce_equality_constraints(q)
#print '-------------------'
#print ''
#
## Q(X) := S(X), X = Y
#r = RelationInQuery('S', {Variable('X'):[0]}, {},[],False)
#q = ConjunctiveQuery([r],[Constraint(Variable('X'), Variable('Y'), '=')],RelationInQuery('S',{Variable('X'):[0]}))
#bla = QueryToAlchemyStatement(q)
#print 'Test 6'
#print 'Original: '
#print q
#print ''
#print bla.reduce_equality_constraints(q)
#print '-------------------'
#print ''
#
## Q(X) := S(Y), X = Y
#r = RelationInQuery('S', {Variable('Y'):[0]}, {},[],False)
#q = ConjunctiveQuery([r],[Constraint(Variable('Y'), Variable('X'), '=')],RelationInQuery('S',{Variable('X'):[0]}))
#bla = QueryToAlchemyStatement(q)
#print 'Test 7'
#print 'Original: '
#print q
#print ''
#print bla.reduce_equality_constraints(q)
#print '-------------------'
#print ''
#
## Q(X) := S(X), P = Y
#
#r = RelationInQuery('S', {Variable('X'):[0]}, {},[],False)
#q = ConjunctiveQuery([r],[Constraint(Variable('Y'), Variable('P'), '=')],RelationInQuery('S',{Variable('X'):[0]}))
#bla = QueryToAlchemyStatement(q)
#print 'Test 8'
#print 'Original: '
#print q
#print ''
#try:
#    print bla.reduce_equality_constraints(q)
#except Exception as e:
#    print e
#print '-------------------'
#print ''
#
#
#s = RelationInQuery('S', {Variable('X'):[0],Variable('Y'):[1]}, {},[],False)
#r = RelationInQuery('R', {Variable('T'):[0],Variable('Z'):[1]}, {},[],False)
#q = ConjunctiveQuery([s,r],[Constraint(Variable('X'), Variable('T'), '='),Constraint(Variable('T'), Variable('X'), '='),Constraint(Variable('Y'), Variable('Z'), '='),Constraint(Variable('T'), Variable('Z'), '='), Constraint(Variable('Z'),Constant('2'), '='),Constraint(Variable('P'), Variable('Q'), '='),Constraint(Variable('P'), Variable('T'), '=')],RelationInQuery('S',{Variable('X'):[0]}))
#bla = QueryToAlchemyStatement(q)
#print 'Test 9'
#print 'Original: '
#print q
#print ''
#print bla.reduce_equality_constraints(q)
#print '-------------------'
#print ''
#
#s = RelationInQuery('S', {Variable('X'):[0,1]}, {},[],False)
#r = RelationInQuery('R', {Variable('T'):[0,1]}, {},[],False)
#q = ConjunctiveQuery([s,r],[Constraint(Variable('X'), Variable('T'), '='),Constraint(Variable('T'), Variable('X'), '='),Constraint(Variable('Y'), Variable('Z'), '='),Constraint(Variable('T'), Variable('Z'), '='), Constraint(Variable('Z'),Constant('2'), '='),Constraint(Variable('P'), Variable('Q'), '='),Constraint(Variable('P'), Variable('T'), '=')],RelationInQuery('S',{Variable('X'):[0]}))
#bla = QueryToAlchemyStatement(q)
#print 'Test 10'
#print 'Original: '
#print q
#print ''
#print bla.reduce_equality_constraints(q)
#print '-------------------'
#print ''
#
## R(X) := S(X), 3=2, X>2
#r = RelationInQuery('S', {Variable('X'):[0]}, {},[],True)
#q = ConjunctiveQuery([r],[Constraint(Constant('3'), Constant('2'), '='),Constraint(Variable('X'), Constant('2'), '>')],RelationInQuery('S',{Variable('X'):[0]}))
#bla = QueryToAlchemyStatement(q)
#print 'Test 11'
#print 'Original: '
#print q
#print ''
#print bla.reduce_equality_constraints(q)
#print '-------------------'
#print ''
#
#s = RelationInQuery('S', {Variable('X'):[0],Variable('P'):[1]}, {},[],False)
#r = RelationInQuery('R', {Variable('T'):[0],Variable('Z'):[1]}, {},[],False)
#q = ConjunctiveQuery([s,r],[Constraint(Variable('X'), Variable('T'), '='),Constraint(Variable('T'), Variable('X'), '='),Constraint(Variable('Y'), Variable('Z'), '='),Constraint(Variable('T'), Variable('Z'), '='), Constraint(Variable('Z'),Constant('2'), '='),Constraint(Variable('P'), Variable('Q'), '='),Constraint(Variable('Y'), Variable('T'), '=')],RelationInQuery('S',{Variable('X'):[0]}))
#bla = QueryToAlchemyStatement(q)
#print 'Test 12'
#print 'Original: '
#print q
#print ''
#print bla.reduce_equality_constraints(q)
#print '-------------------'
#print ''
#
#
#s = RelationInQuery('S', {Variable('X'):[0],Variable('P'):[1]}, {},[],False)
#r = RelationInQuery('R', {Variable('T'):[0],Variable('Z'):[1]}, {},[],False)
#q = ConjunctiveQuery([s,r],[Constraint(Variable('X'), Variable('T'), '='),Constraint(Variable('T'), Variable('X'), '='),Constraint(Variable('Y'), Variable('Z'), '='),Constraint(Variable('T'), Variable('Z'), '='), Constraint(Variable('Z'),Constant('2'), '='),Constraint(Variable('P'), Variable('Q'), '='),Constraint(Variable('Q'), Constant('5'), '=')],RelationInQuery('S',{Variable('X'):[0]}))
#bla = QueryToAlchemyStatement(q)
#print 'Test 13'
#
#print 'Original: '
#print q
#print ''
#print bla.reduce_equality_constraints(q)
#print '-------------------'
#print ''
#
#
## R(X) := S(X), 3=X, X>2
#r = RelationInQuery('S', {Variable('X'):[0]}, {},[],True)
#q = ConjunctiveQuery([r],[Constraint(Constant('3'), Variable('X'), '='),Constraint(Variable('X'), Constant('2'), '>')],RelationInQuery('S',{Variable('X'):[0]}))
#bla = QueryToAlchemyStatement(q)
#print 'Test 14'
#print 'Original: '
#print q
#print ''
#print bla.reduce_equality_constraints(q)
#print '-------------------'
#print ''
#
## R(Y) := S(X), Y=X, X=2 Y =4
#r = RelationInQuery('S', {Variable('Y'):[0]}, {},[],True)
#q = ConjunctiveQuery([r],[Constraint(Variable('Y'), Variable('X'), '='),Constraint(Variable('X'), Constant('2'), '='),Constraint(Variable('Y'), Constant('4'), '=')],RelationInQuery('S',{Variable('Y'):[0]}))
#bla = QueryToAlchemyStatement(q)
#print 'Test 15'
#print 'Original: '
#print q
#print ''
#print bla.reduce_equality_constraints(q)
#print '-------------------'
#print ''
#
## R(X,Y,Z,_,2) := S(X), Y=X, X=2
#r = RelationInQuery('S', {Variable('Y'):[0]}, {},[],True)
#q = ConjunctiveQuery([r],[Constraint(Variable('Y'), Variable('X'), '='),Constraint(Variable('X'), Constant('2'), '='),Constraint(Variable('Y'), Constant('4'), '=')],RelationInQuery('R',{Variable('X'):[0],Variable('Y'):[1],Variable('Z'):[2]},{Constant('2'):[4]},[3]))
#bla = QueryToAlchemyStatement(q)
#print 'Test 16'
#print 'Original: '
#print q
#print ''
#print bla.reduce_equality_constraints(q)
#print '-------------------'
#print ''
#
