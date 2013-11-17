from ASTFactory.ASTBuilder import ASTBuilder
from parserAST.Parser import Parser
from queryExecutor.queryExecutor import QueryExecutor

__author__ = 'caioseguin'

def translateDatalogToSql(datalog_statement):

    datalog_parser = Parser()
    ast_builder = ASTBuilder()
    query_executor = QueryExecutor()
    query_result_list = []

    parsed_statement = datalog_parser.parsesentence(datalog_statement)
    ast_query_list = ast_builder.buildAST(parsed_statement)

    for ast_query in ast_query_list:
        query_result = QueryExecutor().execute_query(ast_query)
        query_result_list.append(query_result)

    return query_result_list