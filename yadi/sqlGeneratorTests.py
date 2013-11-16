import sys
sys.path.append('/home/francisco/DMKM/ADB/repo/yadi/yadi')

from dataStructures.query import *
from dataStructures.relation import *
from dataStructures.element import *
from dataStructures.constraint import *
from queryExecutor.queryExecutor import *
from queryExecutor.sqlFactory import *
from astToSQL import *

def test(list_queries):
    gen = SQLGenerator()
    for i in range(0,len(list_queries)):
        print 'Test :'+ str(i)
        print 'Original:'
        print str(list_queries[i])
        print 'Result:'
        print QueryExecutor().execute_query(list_queries[i])
        print '---------------------------------------------------------'

queries = []

# ------
# Q(X):-!S(Y),X=Y,Y=2
r = RelationInQuery('S', [Variable('Y')],True)
q = ConjunctiveQuery([r],[Constraint(Variable('X'), Variable('Y'), '='),Constraint(Variable('Y'), Constant('2'), '=')],RelationInQuery('Q', [Variable('X')])) 

queries.append(q)

# ------

s = RelationInQuery('S', [Variable('X'),Variable('Y')])
t = RelationInQuery('T', [Variable('X')], True)
queries.append(ConjunctiveQuery([s,t],[Constraint(Variable('Y'), Variable('Z'), '=')],RelationInQuery('Q',[Variable('X'),Variable('Z')]))) 


# ------

test(queries)
