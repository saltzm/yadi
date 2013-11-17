from translateDatalogToSQL import translateDatalogToSql

from evaluate_query import *

__author__ = 'caioseguin'

def main():

    datalog_statement = "q(X,Y)."
    print(translateDatalogToSql(datalog_statement))
    #datalog_statement = "q(X,Y):- s(X,Y). a(X,Y):- b(X,Y)."
    datalog_statement = "m(X,Y):- tuser(X,Y)."

    output = translateDatalogToSql(datalog_statement)
    print(output)
    for sqlS in output:
        evaluateQuery().evaluate(sqlS)

main()
