from ASTFactory.ASTBuilder import *
import sys
sys.path.append('../')

from ASTFactory.ASTBuilder import ASTBuilder
from parserAST.Parser import parser
from queryExecutor.queryExecutor import QueryExecutor

__author__ = 'caioseguin'

def translateDatalogToSql(datalog_statement):

    datalog_parser = parser()
    ast_builder = ASTBuilder()
    query_executor = QueryExecutor()
    sql_query_list = []

    print('Datalog Input:')
    print(datalog_statement)
    print('\n')

    parsed_statement = datalog_parser.parsesentence(datalog_statement)
    ast_query_list = ast_builder.buildAST(parsed_statement.asList())

    for ast_query in ast_query_list:
        sql_query = QueryExecutor().execute_query(ast_query)
        sql_query_list.append(sql_query)

    return sql_query_list
