import sqlalchemy


#from evaluate_query import *
from .dataStructures.query import *
from .dataStructures.relation import *
from .dataStructures.element import *
from .dataStructures.constraint import *
from .queryExecutor.queryExecutor import *
from .queryExecutor.sqlFactory import *


def test(list_queries):
    gen = SQLGenerator()
    for i in range(0,len(list_queries)):
        print ('Test :'+ str(i))
        print ('Original:')
        print (str(list_queries[i]))
        print ('Result:')
        print (QueryExecutor().execute_query(list_queries[i]))
        print ('---------------------------------------------------------')



queries = []

#M(title) :- movie(title,length_min), length_mins>100.
r = RelationInQuery('movie', [Variable('title'),Wildcard(),Variable('length_mins'), Wildcard()], False)
q = ConjunctiveQuery([r], [Constraint(Variable('length_mins'), Constant('100'), '>=')], RelationInQuery('M', [Variable('title')]))

queries.append(q)
# ------
# Q(X):-!S(Y),X=Y,Y=2
r = RelationInQuery('S', [Variable('Y')],True)
q = ConjunctiveQuery([r],[Constraint(Variable('X'), Variable('Y'), '='),Constraint(Variable('Y'), Constant('2'), '=')],RelationInQuery('Q', [Variable('X')]))

queries.append(q)

#------
#Q(X):- S(X)
r = RelationInQuery('S', [Variable('X')])
q = ConjunctiveQuery([r],[],RelationInQuery('Q', [Variable('X')]))
queries.append(q)

# ------
# Q(X):- S(X), X = 2
r = RelationInQuery('S', [Variable('X')])
head = RelationInQuery('Q', [Variable('X')])
queries.append(ConjunctiveQuery([r],[Constraint(Variable('X'),Constant('2'),'=')],head))

# ------

s = RelationInQuery('S', [Variable('X'),Variable('Y')])
t = RelationInQuery('T', [Variable('X')], True)
queries.append(ConjunctiveQuery([s,t],[Constraint(Variable('Y'), Variable('Z'), '=')],RelationInQuery('Q',[Variable('X'),Variable('Z')])))


# ------

# R(X,Y),!S(Z), Y=Z
s = RelationInQuery('R', [Variable('X'),Variable('Y')])
t = RelationInQuery('S', [Variable('Z')], True)

queries.append(ConjunctiveQuery([s,t],[Constraint(Variable('Y'), Variable('Z'), '=')]))

# R(X,Y),!S(Z)

s = RelationInQuery('R', [Variable('X'),Variable('Y')])
t = RelationInQuery('S', [Variable('Z')], True)

queries.append(ConjunctiveQuery([s,t],[]))


# answer(X,Y) :- R(X,A), S(A,Y).

s = RelationInQuery('R', [Variable('X'),Variable('A')])
t = RelationInQuery('S', [Variable('A'),Variable('Y')])
head = RelationInQuery('answer',[Variable('X'),Variable('Y')])
queries.append(ConjunctiveQuery([s,t],[],head))

# answer(X,2) :- R(X,A), S(A,_).

s = RelationInQuery('R', [Variable('X'),Variable('A')])
t = RelationInQuery('S', [Variable('A'),Wildcard()])
head = RelationInQuery('answer',[Variable('X'),Constant('2')])
queries.append(ConjunctiveQuery([s,t],[],head))


# r(_,2)

r = RelationInQuery('answer',[Wildcard(),Constant('2')])
queries.append(ConjunctiveQuery([r],[]))

# R(_,A), S(A,_). -> answer(A) :- R(_,A), S(A,_).

s = RelationInQuery('R', [Wildcard(),Variable('A')])
t = RelationInQuery('S', [Variable('A'),Wildcard()])

queries.append(ConjunctiveQuery([s,t],[]))

# R(X,Y) :- S(X), S(Y), X>Y

s = RelationInQuery('S', [Variable('X')])
t = RelationInQuery('S', [Variable('Y')])
head = RelationInQuery('answer',[Variable('X'),Variable('Y')])
queries.append(ConjunctiveQuery([s,t],[Constraint(Variable('X'),Variable('Y'),'>')],head))

# R(X,Y) :- S(X), Y>2

s = RelationInQuery('S', [Variable('X')])

head = RelationInQuery('answer',[Variable('X'),Variable('Y')])
queries.append(ConjunctiveQuery([s],[Constraint(Variable('Y'),Constant('2'),'>')],head))

# R(X) :- S(X), X<2

s = RelationInQuery('S', [Variable('X')])

head = RelationInQuery('answer',[Variable('X'),Variable('Y')])
queries.append(ConjunctiveQuery([s],[Constraint(Variable('X'),Constant('2'),'<')],head))

# answer(X,Y):-S(X,Z),S(Y,Z),X>Y

s = RelationInQuery('S', [Variable('X'),Variable('Z')])
t = RelationInQuery('S', [Variable('Y'),Variable('Z')])
head = RelationInQuery('answer',[Variable('X'),Variable('Y')])

queries.append(ConjunctiveQuery([s,t],[Constraint(Variable('X'),Variable('Y'),'>')],head))


# R(X) :- X = 2, 3<X

head = RelationInQuery('R',[Variable('X')])

queries.append(ConjunctiveQuery([],[Constraint(Variable('X'),Constant('2'),'='),Constraint(Constant('3'),Variable('X'),'<')],head))

# r(_,2), X = 2

r = RelationInQuery('R',[Wildcard(),Constant('2')])
queries.append(ConjunctiveQuery([r],[Constraint(Variable('X'), Constant('2'), '=')]))

# R(X,Y) :- S(X), S(Y,T), T(X), U(Y), X>Y
s = RelationInQuery('S', [Variable('X')])
t = RelationInQuery('S', [Variable('Y')])
u = RelationInQuery('T', [Variable('X')])
v = RelationInQuery('V', [Variable('Y')])
head = RelationInQuery('answer',[Variable('X'),Variable('Y')])
queries.append(ConjunctiveQuery([s,t,u,v],[Constraint(Variable('X'),Variable('Y'),'>')],head))
test(queries)


