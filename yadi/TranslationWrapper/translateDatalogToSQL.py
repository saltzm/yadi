from ..ASTFactory.ASTBuilder import *

from ..ASTFactory.ASTBuilder import ASTBuilder
from ..parserAST.Parser import parser,SyntaxException
from ..queryExecutor.queryExecutor import QueryExecutor

__author__ = 'caioseguin'

def translateDatalogToSql(datalog_statement):

    datalog_parser = parser()
    ast_builder = ASTBuilder()
    query_executor = QueryExecutor()
    sql_query_list = []

#    print ('-----------------------------')
#    print('Datalog Input:')
#    print(datalog_statement)
#    print('\n')

    try:
        parsed_statement = datalog_parser.parsesentence(datalog_statement)
        ast_query_list = ast_builder.buildAST(parsed_statement.asList())
#        print('Read as :')

        for ast_query in ast_query_list:
            print(str(ast_query))
            sql_query = QueryExecutor().execute_query(ast_query)
            sql_query_list.append(sql_query)
#            print('Generated SQL:')
#            print (sql_query)
    except SyntaxException as e:
        print (e)
    except SafetyException as e:
        print (e)


    return sql_query_list
