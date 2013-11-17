from TranslationWrapper.translateDatalogToSQL import translateDatalogToSql

__author__ = 'caioseguin'

def main():

    datalog_statement = "q(X,Y):- s(X,Y)."
    print(translateDatalogToSql(datalog_statement))

main()
