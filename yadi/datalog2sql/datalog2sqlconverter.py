from .tokens2ast.ast_builder import *
from .parse2tokens.parser import Parser, SyntaxException
from .ast2sql.ast2sqlconverter import Ast2SqlConverter
from .ast2sql.exceptions import *
from colorama import *

__author__ = 'caioseguin', 'saltzm'

class Datalog2SqlConverter:
    def convertDatalog2Sql(self, datalog_statement):
        sql_query_list = []

        try:
            parsed_statement = Parser().parsesentence(datalog_statement)
            ast_query_list = ASTBuilder().buildAST(parsed_statement.asList())

            for ast_query in ast_query_list:
                sql_query = Ast2SqlConverter().convertAst2Sql(ast_query)
                sql_query_list.append(sql_query)
        except SyntaxException as e:
            print (Fore.RED+'SyntaxException: ' + str(e)+Fore.RESET)
        except SafetyException as e:
            print (Fore.RED+'SafetyException: ' + str(e)+Fore.RESET)
        except Exception as e:
            import traceback
            traceback.print_exc()

        return sql_query_list
