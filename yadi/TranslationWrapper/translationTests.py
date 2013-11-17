
from .translateDatalogToSQL import translateDatalogToSql

from ..evaluate_query import *

__author__ = 'caioseguin'

def main():
    datatog_statements = []
    datatog_statements.append('users(X,Y):- tuser(X,Y).')
    datatog_statements.append('users(Y,L):-tuser(_,Y,_,L).')
    datatog_statements.append("users(Y):-tuser(_,Y,_,L), L='Lyon'.")
    #datatog_statements.append('q(X):-not(s(Y)),X=Y,Y=2.')
    #datatog_statements.append('q(X):- s(X), X = 2.')
    #datatog_statements.append('r(X,Y),!s(Z), Y=Z.')
    #datatog_statements.append('r(X,Y),!s(Z).')
    #datatog_statements.append('a(X,Y) :- r(X,A), s(A,Y).')
    #datatog_statements.append('a(X,2) :- r(X,A), s(A,_).')
    #datatog_statements.append('r(_,2).')
    #datatog_statements.append('r(_,A), s(A,_)..')
    #datatog_statements.append('r(X,Y) :- s(X), s(Y), X>Y.')
    #datatog_statements.append('r(X,Y) :- s(X), Y>2')
    #datatog_statements.append('r(X) :- s(X), X<2')
    #datatog_statements.append('a(X,Y):-s(X,Z),s(Y,Z),X>Y.')
    #datatog_statements.append('s(X) :- X = 2, 3<X.')
    #datatog_statements.append('r(_,2), X = 2.')
    #datatog_statements.append('a(X,Y) :- s(X), sa(Y,T), t(X), u(Y), X>Y.')
    #datatog_statements.append("q(X,Y):- s(X,Y). a(X,Y):- b(X,Y).")

    sql_list=[]
    for d_query in datatog_statements:
        #print(translateDatalogToSql(d_query))
        s = translateDatalogToSql(d_query)
        sql_list.append(s[0])

    for sqlS in sql_list:
        evaluateQuery().evaluate(sqlS)


main()
