#  Q(X) := not S(Y), X = Y, X = 2
r = RelationInQuery('S', {Variable('Y'):[0]}, {},[],True)
q = Query([r],[[Variable('X'), Variable('Y'), '='],[Variable('X'), Constant('2'), '=']],{Variable('X'):[0]}) 
bla = QueryToAlchemyStatement(q)
print 'Test 5'
print 'Original: '
print q
print ''
print bla.reduce_equality_constraints(q)
print '-------------------'
print ''

print bla.generateAlchemyStatement()
