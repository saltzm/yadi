from ..ast_factory.ASTBuilder import *
from ..parser_ast.Parser import parser,SyntaxException
from ..query_executor.queryExecutor import QueryExecutor
from ..query_executor.exceptions import *
from colorama import *

__author__ = 'caioseguin'

class Datalog2SqlConverter:
    def convertDatalogToSql(datalog_statement):
        datalog_parser = parser()
        ast_builder = ASTBuilder()
        query_executor = QueryExecutor()
        sql_query_list = []

        try:
            parsed_statement = datalog_parser.parsesentence(datalog_statement)
            ast_query_list = ast_builder.buildAST(parsed_statement.asList())

            for ast_query in ast_query_list:
                sql_query = QueryExecutor().execute_query(ast_query)
                sql_query_list.append(sql_query)
        except SyntaxException as e:
            print (Fore.RED+'SyntaxException: ' + str(e)+Fore.RESET)
        except SafetyException as e:
            print (Fore.RED+'SafetyException: ' + str(e)+Fore.RESET)
        except Exception as e:
            import traceback
            traceback.print_exc()

        return sql_query_list
