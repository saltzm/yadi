from .tokens2ast.ast_builder import *
from .parse2tokens.parser import Parser, SyntaxException
from .ast2sql.ast2sqlconverter import Ast2SqlConverter
from .ast2sql.exceptions import *
from ..sql_engine.db_state_tracker import DBStateTracker
from colorama import *

__author__ = 'caioseguin', 'saltzm'

class Datalog2SqlConverter:
    def __init__(self, db_state_tracker):
        self.db_state_tracker = db_state_tracker

    def convertDatalog2Sql(self, datalog_statement, is_assertion = False):
        sql_query_list = []

        try:
            parsed_statement = Parser().parsesentence(datalog_statement).asList()
            ast_query_list = ASTBuilder().buildAST(
                                parsed_statement,
                                is_assertion
                             )

            for ast_query in ast_query_list:
                sql_query = \
                    Ast2SqlConverter(self.db_state_tracker).convertAst2Sql(ast_query)
                sql_query_list.append(sql_query)
        except SyntaxException as e:
            print (Fore.RED+'SyntaxException: ' + str(e)+Fore.RESET)
        except SafetyException as e:
            print (Fore.RED+'SafetyException: ' + str(e)+Fore.RESET)
        except Exception as e:
            import traceback
            traceback.print_exc()

        return sql_query_list
    def trim_assert(self, statement):
        return statement[len('/assert '):]
