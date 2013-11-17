import sys
sys.path.append('/home/nishara/PycharmProjects/yadi/yadi/')

from translateDatalogToSQL import translateDatalogToSql

from evaluate_query import *

__author__ = 'caioseguin'

def main():
    datatog_statements = []
    datalog_statements.append('q(X):-not(s(Y)),X=Y,Y=2.')
    datalog_statements.append('q(X):- s(X), X = 2.')
    datalog_statements.append('r(X,Y),!s(Z), Y=Z.')
    datalog_statements.append('r(X,Y),!s(Z).')
    datalog_statements.append('a(X,Y) :- r(X,A), s(A,Y).')
    datalog_statements.append('a(X,2) :- r(X,A), s(A,_).')
    datalog_statements.append('r(_,2).')
    datalog_statements.append('r(_,A), s(A,_)..')
    datalog_statements.append('r(X,Y) :- s(X), s(Y), X>Y.')
    datalog_statements.append('r(X,Y) :- s(X), Y>2')
    datalog_statements.append('r(X) :- s(X), X<2')
    datalog_statements.append('a(X,Y):-s(X,Z),s(Y,Z),X>Y.')
    datalog_statements.append('s(X) :- X = 2, 3<X.')
    datalog_statements.append('r(_,2), X = 2.')
    datalog_statements.append('a(X,Y) :- s(X), sa(Y,T), t(X), u(Y), X>Y.')
    datalog_statements.append("q(X,Y):- s(X,Y). a(X,Y):- b(X,Y).")

    #datalog_statement = "q(X,Y):- s(X,Y). a(X,Y):- b(X,Y)."
    datalog_statement = "m(X,Y):- tuser(X,Y)."

    output = translateDatalogToSql(datalog_statement)
    print(output)
    for sqlS in output:
        evaluateQuery().evaluate(sqlS)
    for test in datalog_statements:
        print(translateDatalogToSql(datalog_statement))

main()
